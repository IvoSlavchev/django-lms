from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

class Course(models.Model):
	owner = models.CharField(max_length=30)
	name = models.CharField(max_length=30, unique=True, db_index=True)
	description = models.TextField(blank=True)
	created = models.DateTimeField(default=datetime.now)
	participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through='Participation')

class Participation(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)