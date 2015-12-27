from django.conf.urls import include, url
from django.contrib import admin

from users import urls as users_urls
from courses import urls as courses_urls

urlpatterns = [
	url(r'^', include(users_urls)),
	url(r'^courses/', include(courses_urls)),
]