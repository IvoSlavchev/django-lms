from django.conf.urls import url

from users import views

urlpatterns = [
	url(r'^$', views.home_page, name='home'),
    url(r'^teacher', views.teacher_page, name='teacher'),
    url(r'^student', views.student_page, name='student'),
]