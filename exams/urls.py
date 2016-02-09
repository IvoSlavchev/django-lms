from django.conf.urls import url

from exams import views


urlpatterns = [
    url(r'^$', views.list_exams, name='list_exams'),
    url(r'^create$', views.create_exam, name='create_exam'),
    url(r'^(?P<exam_id>\d+)$', views.edit_exam, name='edit_exam'),
    url(r'^(?P<exam_id>\d+)/results$', views.view_exam_results,
        name='view_exam_results'),
    url(r'^(?P<exam_id>\d+)/result/(?P<student_id>\d+)$',
        views.view_participant_result, name='view_participant_result'),
    url(r'^(?P<exam_id>\d+)/questions$', views.view_assigned,
    	name='view_assigned'),
    url(r'^(?P<exam_id>\d+)/s$', views.view_exam, name='view_exam'),
    url(r'^(?P<exam_id>\d+)/p$', views.input_password, name='input_password'),
    url(r'^(?P<exam_id>\d+)/t$', views.take_exam, name='take_exam'),
    url(r'^(?P<exam_id>\d+)/result/s$', views.view_result,
    	name='view_result'),
]