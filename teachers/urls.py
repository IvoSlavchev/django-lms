from django.conf.urls import url

from teachers import views

urlpatterns = [
	url(r'^$', views.dashboard, name='teacher_dashboard'),
	url(r'^(\d+)/$', views.edit_course, name='edit_course'),
	url(r'^create/$', views.create, name='create'),
]