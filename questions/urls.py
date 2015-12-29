from django.conf.urls import url

from questions import views

urlpatterns = [
	url(r'^create$', views.create_question, name='create_question'),
	url(r'^(\d+)$', views.edit_question, name='edit_question'),	
]