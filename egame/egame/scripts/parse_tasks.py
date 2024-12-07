import json
import re

import bs4
import requests
from tqdm import tqdm

"""
Запускать через терминал (python parse_tasks.py),
иначе прогресбары на работают, сохраняет фикстуру
в fixtures/tasks.json, константы тут в большом
количестве к сожалению неизбежны, возможно
следуют их вообще вынести в .env или конфиг,
для запуска нужны зависимости из dev.txt
"""

EXAMS = {
    "Русский язык": 2,
    "Математика": 1,
    "Физика": 4,
}

ROOT_URL = "https://3.shkolkovo.online"
OUTPUT_PATH = "../../fixtures/tasks.json"
APP_NAME = "practice"

pk_counter = {
    "exam": 1,
    "theme": 1,
    "subtopic": 1,
    "task": 1,
    "answer": 1,
}

theme_progress = tqdm(total=73, desc="Themes", position=3)
subtopic_progress = tqdm(total=647, desc="Subtopics", position=2)
task_progress = tqdm(total=9313, desc="Tasks", position=1)


def add_host_to_links(html_fragment):
    return re.sub(r'(?<=src=["\'])/(?!/)', f"{ROOT_URL}/", str(html_fragment))


fixture = []

for exam_name, subject_id in EXAMS.items():
    tqdm.write(f"Processing exam: {exam_name}")

    fixture.append(
        {
            "model": f"{APP_NAME}.exam",
            "pk": pk_counter["exam"],
            "fields": {
                "name": exam_name,
            },
        }
    )
    current_exam_id = pk_counter["exam"]
    pk_counter["exam"] += 1

    response = requests.get(f"{ROOT_URL}/catalog?SubjectId={subject_id}").text
    soup = bs4.BeautifulSoup(response, "lxml")
    themes_divs = soup.find_all("div", class_="jsx-1658459108 accordion__item")

    for theme_index, theme_div in enumerate(themes_divs, start=1):
        theme_name = theme_div.find(
            "div", class_="jsx-1658459108 accordion__title-wrap"
        ).text

        match exam_name:
            case "Математика":
                answered_range = range(1, 13)
            case "Физика":
                answered_range = range(1, 24)
            case "Русский язык":
                answered_range = range(1, 27)
            case _:
                answered_range = range(1, 10)

        fixture.append(
            {
                "model": f"{APP_NAME}.theme",
                "pk": pk_counter["theme"],
                "fields": {
                    "name": theme_name,
                    "task_number": theme_index,
                    "exam": current_exam_id,
                    "is_answered": theme_index in answered_range,
                },
            }
        )
        current_theme_id = pk_counter["theme"]
        pk_counter["theme"] += 1

        subtopics_a = theme_div.find_all("a", class_="jsx-549154022")
        for subtopic_index, subtopic_a in enumerate(subtopics_a[:-1], start=1):
            subtopic_name = subtopic_a.text
            subtopic_url = ROOT_URL + subtopic_a.get("href")

            fixture.append(
                {
                    "model": f"{APP_NAME}.subtopic",
                    "pk": pk_counter["subtopic"],
                    "fields": {
                        "name": subtopic_name,
                        "number": subtopic_index,
                        "theme": current_theme_id,
                    },
                }
            )
            current_subtopic_id = pk_counter["subtopic"]
            pk_counter["subtopic"] += 1

            response = requests.get(subtopic_url).text
            tasks_soup = bs4.BeautifulSoup(response, "lxml")
            tasks_divs = tasks_soup.find_all("div", class_="exercise")

            for task_div in tasks_divs:
                try:
                    try:
                        task_html = task_div.find(
                            "div", class_="exercise__text"
                        )
                        try:
                            task_html = task_html.find(
                                "div", class_="tex-render"
                            ).decode_contents()
                        except AttributeError:
                            pass

                    except AttributeError:
                        task_html = task_div.find(
                            "div", class_="questionContent public-catalog"
                        ).decode_contents()

                    task_html = add_host_to_links(task_html)

                    task_solution_html = add_host_to_links(
                        task_div.find("div", class_="exercise__solution-text")
                        .find("div", class_="tex-render")
                        .decode_contents()
                    )

                    fixture.append(
                        {
                            "model": f"{APP_NAME}.task",
                            "pk": pk_counter["task"],
                            "fields": {
                                "task_text_html": task_html,
                                "task_solution_html": task_solution_html,
                            },
                        }
                    )

                    current_task_id = pk_counter["task"]
                    pk_counter["task"] += 1
                    answers = task_div.find_all(
                        ["span", "li"], class_="answer"
                    )

                    for answer in answers:
                        try:
                            fixture.append(
                                {
                                    "model": f"{APP_NAME}.answer",
                                    "pk": pk_counter["answer"],
                                    "fields": {
                                        "answer": answer.text,
                                        "task": current_task_id,
                                    },
                                }
                            )
                            pk_counter["answer"] += 1
                        except AttributeError:
                            pass

                    task_progress.update(1)

                except AttributeError:
                    pass

            subtopic_progress.update(1)
        theme_progress.update(1)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(fixture, f, ensure_ascii=False, indent=4)

tqdm.write("Completed 🌟!")
