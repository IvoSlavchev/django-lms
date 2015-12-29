from django.db import models

from courses.models import Course

class Exam(models.Model):
	
	owner = models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	description = models.TextField(blank=True)
	updated = models.DateTimeField(auto_now=True)
	date_to_be_taken = models.DateTimeField()
	course = models.ForeignKey(Course)