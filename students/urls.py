from django.conf.urls import url

from students import views

urlpatterns = [
	url(r'^$', views.dashboard, name='student_dashboard'),
	url(r'^(\d+)/$', views.view_course, name='view_course'),
]