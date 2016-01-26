from django.contrib import admin

from exams.models import Exam, ExamQuestion, Score, StudentAnswer

admin.site.register(Exam)
admin.site.register(ExamQuestion)
admin.site.register(Score)
admin.site.register(StudentAnswer)