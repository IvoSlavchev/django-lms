from django.utils import timezone

from django.conf import settings
from django.db import models

from courses.models import Course
from questions.models import Question


class Exam(models.Model):
    
    owner = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=10, blank=True)
    time_limit = models.TimeField()
    active_from = models.DateTimeField()
    active_to = models.DateTimeField()
    course = models.ForeignKey(Course)
    questions = models.ManyToManyField(Question, blank=True,
        through='ExamQuestion')

    @property
    def activated(self):
        return timezone.now() >= self.active_from

    @property
    def expired(self):
        return timezone.now() > self.active_to


class ExamQuestion(models.Model):

    question = models.ForeignKey(Question)
    exam = models.ForeignKey(Exam)


class Score(models.Model):

    student = models.ForeignKey(settings.AUTH_USER_MODEL)
    exam = models.ForeignKey(Exam)
    score = models.IntegerField()