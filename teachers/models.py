from django.conf import settings
from django.db import models
from datetime import datetime

class Course(models.Model):
	owner = models.CharField(max_length=30)
	name = models.CharField(max_length=30, unique=True, db_index=True)
	description = models.TextField()
	created = models.DateTimeField(default=datetime.now)