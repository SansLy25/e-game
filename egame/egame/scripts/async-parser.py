import asyncio
from itertools import chain
import json
from pathlib import Path
import re

import aiohttp
import selectolax.parser
from tqdm.asyncio import tqdm

__all__ = ()


EXAMS = {
    "Русский язык": 2,
    "Математика": 1,
    "Физика": 4,
}

ROOT_URL = "https://3.shkolkovo.online"
OUTPUT_PATH = Path("egame/fixtures/async-tasks.json")
APP_NAME = "practice"

SRC_REGEX = re.compile(r'(?<=src=["\'])/(?!/)')

EXAMS_SEMAPHORE_LIMIT = 1
THEMES_SEMAPHORE_LIMIT = 2
SUBTOPICS_SEMAPHORE_LIMIT = 10
TASKS_SEMAPHORE_LIMIT = 20
ANSWERS_SEMAPHORE_LIMIT = 50

MAX_ATTEMPTS_COUNT = 5
TIMEOUT = 2

theme_bar = tqdm(total=71, desc="Themes", position=1)
subtopic_bar = tqdm(total=648, desc="Subtopics", position=2)
task_bar = tqdm(total=9358, desc="Tasks", position=3)

pk_lock = asyncio.Lock()
pk_counter = {
    "exam": 0,
    "theme": 0,
    "subtopic": 0,
    "task": 0,
    "answer": 0,
}


async def increment_pk_counter(key) -> int:
    async with pk_lock:
        pk_counter[key] += 1
        return pk_counter[key]


def limited_task(value: int):
    semaphore = asyncio.Semaphore(value)

    def decorator(coro):
        async def wrapper(*args, **kwargs):
            async with semaphore:
                return await coro(*args, **kwargs)

        return wrapper

    return decorator


async def fetch_url(url, session: aiohttp.ClientSession) -> str:
    for _ in range(MAX_ATTEMPTS_COUNT):
        try:
            async with session.get(url, timeout=TIMEOUT) as response:
                response.raise_for_status()
                return await response.text()
        except asyncio.TimeoutError:
            continue

    raise aiohttp.ClientError(
        f"Failed to fetch `{url}` after {MAX_ATTEMPTS_COUNT} attempts",
    )


def add_host_to_links(html_fragment: str) -> str:
    return SRC_REGEX.sub(f"{ROOT_URL}/", html_fragment)


@limited_task(EXAMS_SEMAPHORE_LIMIT)
async def get_exam(
    exam_name: str,
    subject_id: int,
    session: aiohttp.ClientSession,
):
    tqdm.write(f"Processing exam: {exam_name}")

    themes = selectolax.parser.HTMLParser(
        await fetch_url(
            f"{ROOT_URL}/catalog?SubjectId={subject_id}",
            session,
        ),
    ).css("div.jsx-1658459108.accordion__item")

    match exam_name:
        case "Математика":
            answered_range = range(1, 13)
        case "Физика":
            answered_range = range(1, 24)
        case "Русский язык":
            answered_range = range(1, 27)
        case _:
            answered_range = range(1, 10)

    return [
        {
            "model": f"{APP_NAME}.exam",
            "pk": await increment_pk_counter("exam"),
            "fields": {
                "name": exam_name,
            },
        },
    ] + list(
        chain.from_iterable(
            await asyncio.gather(
                *(
                    get_theme(
                        theme,
                        theme_index,
                        pk_counter["exam"],
                        answered_range,
                        session,
                    )
                    for theme_index, theme in enumerate(
                        themes,
                        start=1,
                    )
                ),
            ),
        ),
    )


@limited_task(THEMES_SEMAPHORE_LIMIT)
async def get_theme(
    theme: selectolax.parser.Node,
    theme_index: int,
    exam_id: int,
    answered_range: str,
    session: aiohttp.ClientSession,
):
    theme_bar.update()

    subtopics = theme.css("a.jsx-549154022")[:-1]
    return [
        {
            "model": f"{APP_NAME}.theme",
            "pk": await increment_pk_counter("theme"),
            "fields": {
                "name": theme.css_first(
                    "div.jsx-1658459108.accordion__title-wrap",
                ).text(),
                "task_number": theme_index,
                "exam": exam_id,
                "is_answered": theme_index in answered_range,
            },
        },
    ] + list(
        chain.from_iterable(
            await asyncio.gather(
                *(
                    get_subtopic(
                        subtopic_a,
                        subtopic_index,
                        theme_index,
                        session,
                    )
                    for subtopic_index, subtopic_a in enumerate(
                        subtopics,
                        start=1,
                    )
                ),
            ),
        ),
    )


@limited_task(SUBTOPICS_SEMAPHORE_LIMIT)
async def get_subtopic(
    subtopic_a: selectolax.parser.Node,
    subtopic_index: int,
    theme_index: int,
    session: aiohttp.ClientSession,
):
    subtopic_bar.update()

    text = await fetch_url(
        ROOT_URL + subtopic_a.attributes.get("href"),
        session,
    )
    tasks = selectolax.parser.HTMLParser(text).css("div.exercise")

    return [
        {
            "model": f"{APP_NAME}.subtopic",
            "pk": await increment_pk_counter("subtopic"),
            "fields": {
                "name": subtopic_a.text(),
                "number": subtopic_index,
                "theme": theme_index,
            },
        },
    ] + list(
        chain.from_iterable(
            await asyncio.gather(*(get_task(task) for task in tasks)),
        ),
    )


@limited_task(TASKS_SEMAPHORE_LIMIT)
async def get_task(task: selectolax.parser.Node):
    task_bar.update()

    task_html_node = task.css_first("div.exercise__text")
    if task_html_node:
        tex_render = task_html_node.css_first("div.tex-render")
        task_html = tex_render.html if tex_render else task_html_node.html
    else:
        task_html_node = task.css_first(
            "div.questionContent.public-catalog",
        )
        task_html = task_html_node.html if task_html_node else None

    if task_html:
        task_html = add_host_to_links(task_html)

    solution_node = task.css_first(
        "div.exercise__solution-text div.tex-render",
    )
    solution_html = (
        add_host_to_links(solution_node.html) if solution_node else None
    )

    if task_html is None or solution_html is None:
        return []

    return [
        {
            "model": f"{APP_NAME}.task",
            "pk": await increment_pk_counter("task"),
            "fields": {
                "task_text_html": task_html,
                "task_solution_html": solution_html,
            },
        },
    ] + await asyncio.gather(
        *(
            get_answer(answer, pk_counter["task"])
            for answer in task.css("span.answer, li.answer")
        ),
    )


@limited_task(ANSWERS_SEMAPHORE_LIMIT)
async def get_answer(answer: selectolax.parser.Node, task_id):
    return {
        "model": f"{APP_NAME}.answer",
        "pk": await increment_pk_counter("answer"),
        "fields": {
            "answer": answer.text(),
            "task": task_id,
        },
    }


async def main():
    if not OUTPUT_PATH.exists():
        raise FileNotFoundError(OUTPUT_PATH)

    async with aiohttp.ClientSession() as session:
        data = list(
            chain.from_iterable(
                await asyncio.gather(
                    *(
                        get_exam(exam_name, subject_id, session)
                        for exam_name, subject_id in EXAMS.items()
                    ),
                ),
            ),
        )

        with OUTPUT_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    tqdm.write("Completed 🌟!")


if __name__ == "__main__":
    asyncio.run(main())
