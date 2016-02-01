from django.utils import timezone

from django.conf import settings
from django.db import models

from courses.models import Course
from questions.models import Question


class Exam(models.Model):
    
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=10, blank=True)
    time_limit = models.TimeField()
    active_from = models.DateTimeField()
    active_to = models.DateTimeField()
    course = models.ForeignKey(Course)
    category = models.CharField(max_length=30)
    question_count = models.IntegerField()
    questions = models.ManyToManyField(Question, blank=True,
        through='ExamQuestion')

    @property
    def active(self):
        return (timezone.now() >= self.active_from and
            timezone.now() < self.active_to)

    def __str__(self):
        return self.name


class ExamQuestion(models.Model):

    question = models.ForeignKey(Question)
    exam = models.ForeignKey(Exam)

    def __str__(self):
        return '{} for {}'.format(self.question, self.exam)


class Score(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    exam = models.ForeignKey(Exam)
    score = models.IntegerField()

    def __str__(self):
        return '{} for {}'.format(self.user, self.exam)


class StudentAnswer(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    exam_question = models.ForeignKey(ExamQuestion)
    answer = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} for {} for {}'.format(self.user,
            self.exam_question.question, self.exam_question.exam)