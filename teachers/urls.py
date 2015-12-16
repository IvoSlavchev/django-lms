from django.conf.urls import url

from teachers import views

urlpatterns = [
	url(r'^$', views.dashboard, name='teacher_dashboard'),
	url(r'^(\d+)/$', views.view_course, name='view_course'),
	url(r'^create/$', views.create, name='create'),
]