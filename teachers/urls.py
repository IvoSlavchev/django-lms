from django.conf.urls import url

from teachers import views

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'),
	url(r'^create/$', views.create, name='create'),
]