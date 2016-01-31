from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class Course(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner')
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
        through='Participation')

    def __str__(self):
        return self.name


class Participation(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    course = models.ForeignKey(Course)

    def __str__(self):
        return '{} for {}'.format(self.user, self.course)