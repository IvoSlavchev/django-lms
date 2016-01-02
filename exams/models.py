from django.conf import settings
from django.db import models

from courses.models import Course
from questions.models import Question

class Exam(models.Model):
	
	owner = models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	description = models.TextField(blank=True)
	updated = models.DateTimeField(auto_now=True)
	date_to_be_taken = models.DateTimeField()
	course = models.ForeignKey(Course)
	questions = models.ManyToManyField(Question, blank=True, through='ExamQuestion')

class ExamQuestion(models.Model):

	question = models.ForeignKey(Question)
	exam = models.ForeignKey(Exam)

class Score(models.Model):

	student = models.ForeignKey(settings.AUTH_USER_MODEL)
	exam = models.ForeignKey(Exam)
	score = models.IntegerField()