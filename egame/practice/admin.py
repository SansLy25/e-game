from django.contrib import admin

from practice import models

admin.site.register(models.Exam)
admin.site.register(models.Theme)
admin.site.register(models.Subtopic)
admin.site.register(models.Task)
admin.site.register(models.Answer)
admin.site.register(models.Solution)
admin.site.register(models.Variant)
