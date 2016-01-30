from django.conf.urls import url, include

from courses import views


urlpatterns = [
    url(r'^$', views.teacher_courses, name='teacher_courses'),
    url(r'^create$', views.create_course, name='create_course'),
    url(r'^(?P<course_id>\d+)$', views.edit_course, name='edit_course'),
    url(r'^(?P<course_id>\d+)/participants$', views.edit_participants,
        name='edit_participants'),
    url(r'^(?P<course_id>\d+)/results$', views.view_course_results, 
    	name='view_course_results'),
    url(r'^s', views.student_courses, name='student_courses'),
    url(r'^(?P<course_id>\d+)/s$', views.view_course, name='view_course'),
]