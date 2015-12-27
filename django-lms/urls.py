from django.conf.urls import include, url
from django.contrib import admin

from courses import urls as courses_urls
from exams import urls as exams_urls
from users import urls as users_urls

urlpatterns = [
	url(r'^', include(users_urls)),
	url(r'^courses/', include(courses_urls)),
	url(r'^(\d+)/exams/', include(exams_urls)),
]