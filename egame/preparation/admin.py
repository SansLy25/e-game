import django.contrib

import practice.models
import preparation.models


class TaskInline(django.contrib.admin.TabularInline):
    model = preparation.models.Task
    extra = 1
    fields = (
        preparation.models.Task.order.field.name,
        preparation.models.Task.question.field.name,
        preparation.models.Task.correct_answer.field.name,
        preparation.models.Task.options.field.name,
    )


@django.contrib.admin.register(preparation.models.Test)
class TestAdmin(django.contrib.admin.ModelAdmin):
    exam_field = preparation.models.Test.exam.field.name
    name_field = practice.models.Exam.name.field.name

    list_display = (
        preparation.models.Test.title.field.name,
        exam_field,
    )

    search_fields = (
        preparation.models.Test.title.field.name,
        f"{exam_field}__{name_field}",
    )
    list_filter = (exam_field,)
    inlines = [TaskInline]


@django.contrib.admin.register(preparation.models.Task)
class TaskAdmin(django.contrib.admin.ModelAdmin):
    test_field = preparation.models.Task.test.field.name
    exam_field = preparation.models.Test.exam.field.name
    name_field = practice.models.Exam.name.field.name
    title_field = preparation.models.Test.title.field.name
    order_field = preparation.models.Task.order.field.name
    question_field = preparation.models.Task.question.field.name

    list_display = (
        "get_exam",
        test_field,
        order_field,
        question_field,
        preparation.models.Task.correct_answer.field.name,
    )
    search_fields = (
        question_field,
        f"{test_field}__{title_field}",
        f"{test_field}__{exam_field}__{name_field}",
    )
    list_filter = (f"{test_field}__{exam_field}",)

    ordering = (
        test_field,
        order_field,
    )

    def get_exam(self, obj):
        return obj.test.exam

    get_exam.short_description = "Exam"
    get_exam.admin_order_field = f"{test_field}__{exam_field}"


__all__ = ()
