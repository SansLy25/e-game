import django.contrib

import preparation.models


@django.contrib.admin.register(preparation.models.Exam)
class ExamAdmin(django.contrib.admin.ModelAdmin):
    list_display = (preparation.models.Exam.name.field.name,)
    ordering = (preparation.models.Exam.name.field.name,)


@django.contrib.admin.register(preparation.models.Task)
class TaskAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        preparation.models.Task.question.field.name,
        preparation.models.Task.exam.field.name,
        preparation.models.Task.correct_answer.field.name,
    )
    list_filter = (preparation.models.Task.exam.field.name,)

    task_question_field = preparation.models.Task.question.field.name

    task_field_name = preparation.models.Task.exam.field.name
    exam_name_field_name = preparation.models.Exam.name.field.name
    exam_name_field = f"{task_field_name}__{exam_name_field_name}"

    search_fields = (task_question_field, exam_name_field)
    ordering = (
        preparation.models.Task.exam.field.name,
        preparation.models.Task.id.field.name,
    )

    task_fields = (
        preparation.models.Task.exam.field.name,
        preparation.models.Task.question.field.name,
        preparation.models.Task.correct_answer.field.name,
        preparation.models.Task.options.field.name,
    )

    fieldsets = ((None, {"fields": task_fields}),)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "options":
            kwargs["widget"] = (
                django.contrib.admin.widgets.AdminTextareaWidget()
            )

        return super().formfield_for_dbfield(db_field, **kwargs)


__all__ = ()
