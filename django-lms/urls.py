from django.conf.urls import include, url

from courses import urls as courses_urls
from exams import urls as exams_urls
from questions import urls as questions_urls
from users import urls as users_urls

urlpatterns = [
	url(r'^', include(users_urls)),
	url(r'^courses/', include(courses_urls)),
	url(r'^courses/(\d+)/exams/', include(exams_urls)),
	url(r'^courses/(\d+)/questions/', include(questions_urls)),
]