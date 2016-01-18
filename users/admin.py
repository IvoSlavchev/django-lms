from django.contrib import admin

from users.models import User, UserProfile

admin.site.register(User)
admin.site.register(UserProfile)