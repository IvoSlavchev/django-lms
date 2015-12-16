from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

class Course(models.Model):
	owner = models.CharField(max_length=30)
	name = models.CharField(max_length=30, unique=True, db_index=True)
	description = models.TextField(blank=True)
	created = models.DateTimeField(default=datetime.now)

	def get_absolute_url(self):
		return reverse('view_course', args=[self.id])