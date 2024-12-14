import django.contrib

import practice.models
import preparation.models


class TaskInline(django.contrib.admin.TabularInline):
    model = preparation.models.Task
    extra = 1


@django.contrib.admin.register(preparation.models.Test)
class TestAdmin(django.contrib.admin.ModelAdmin):
    exam_field = preparation.models.Test.exam.field.name
    name_field = practice.models.Exam.name.field.name

    list_display = (
        preparation.models.Test.title.field.name,
        preparation.models.Test.exam.field.name,
    )

    search_fields = (
        preparation.models.Test.title.field.name,
        f"{exam_field}__{name_field}",
    )
    list_filter = (preparation.models.Test.exam.field.name,)
    inlines = [TaskInline]


@django.contrib.admin.register(preparation.models.Task)
class TaskAdmin(django.contrib.admin.ModelAdmin):
    test_field = preparation.models.Task.test.field.name
    exam_field = preparation.models.Test.exam.field.name
    name_field = practice.models.Exam.name.field.name
    title_field = preparation.models.Test.title.field.name

    list_display = (
        "get_exam",
        preparation.models.Task.test.field.name,
        preparation.models.Task.question.field.name,
        preparation.models.Task.correct_answer.field.name,
    )
    search_fields = (
        preparation.models.Task.question.field.name,
        f"{test_field}__{title_field}",
        f"{test_field}__{exam_field}__{name_field}",
    )  # Поля для поиска
    list_filter = (f"{test_field}__{exam_field}",)

    def get_exam(self, obj):
        return obj.test.exam

    get_exam.short_description = "Exam"
    get_exam.admin_order_field = f"{test_field}__{exam_field}"


__all__ = ()
