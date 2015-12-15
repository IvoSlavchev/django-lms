from django.conf.urls import url

from users import views

urlpatterns = [
	url(r'^$', views.home_page, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]