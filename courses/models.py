from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class Course(models.Model):

	owner = models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
		through='Participation')


class Participation(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	course = models.ForeignKey(Course)