from django.conf.urls import url

from courses import views

urlpatterns = [
	url(r'^teacher/$', views.teacher_page, name='teacher_page'),
	url(r'^teacher/(\d+)', views.edit_course, name='edit_course'),
	url(r'^teacher/create/$', views.create_course, name='create_course'),
	url(r'^student/$', views.student_page, name='student_page'),
	url(r'^student/(\d+)', views.view_course, name='view_course'),
]