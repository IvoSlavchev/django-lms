from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models

class User(AbstractBaseUser):

	username = models.CharField(max_length=30, unique=True)
	email = models.EmailField(max_length=30, unique=True)
	is_teacher = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=timezone.now)
	is_active = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'

	objects = UserManager()

	def __unicode__(self):
		return self.username

class UserProfile(models.Model):

	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length=40)
	key_expires = models.DateTimeField(default=timezone.now)