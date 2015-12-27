from django.conf.urls import url

from exams import views

urlpatterns = [
	url(r'^create/$', views.create_exam, name='create_exam'),
]