from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models

class User(AbstractBaseUser):

	username = models.CharField(max_length=30, unique=True, db_index=True)
	email = models.EmailField(max_length=30)
	is_teacher = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=datetime.now)
	is_active = models.BooleanField(default=True)

	USERNAME_FIELD = 'username'

	objects = UserManager()

	def __unicode__(self):
		return self.username

class UserProfile(models.Model):

	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length=40, default='')
	key_expires = models.DateTimeField(default=datetime.now)