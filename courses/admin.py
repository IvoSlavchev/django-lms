from django.contrib import admin

from courses.models import Course, Participation

admin.site.register(Course)
admin.site.register(Participation)