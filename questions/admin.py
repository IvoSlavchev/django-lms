from django.contrib import admin

from questions.models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)