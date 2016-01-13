from django.conf.urls import url

from questions import views


urlpatterns = [
    url(r'^$', views.list_questions, name='list_questions'),
    url(r'^create$', views.create_question, name='create_question'),
    url(r'^(?P<question_id>\d+)$', views.edit_question, name='edit_question'),
]