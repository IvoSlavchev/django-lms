from django.utils import timezone

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):

    is_teacher = models.BooleanField(default=False)


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username