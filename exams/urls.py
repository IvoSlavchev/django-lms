from django.conf.urls import url

from exams import views

urlpatterns = [
	url(r'^create$', views.create_exam, name='create_exam'),
	url(r'^(\d+)$', views.edit_exam, name='edit_exam'),	
	url(r'^(\d+)/s$', views.view_exam, name='view_exam'),
]