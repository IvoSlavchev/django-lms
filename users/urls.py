from django.conf.urls import url
from django.contrib.auth import views as auth_views

from users import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^confirm$', views.confirm, name='confirm'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^profile$', auth_views.password_change, 
    	{'template_name': 'profile.html', 'post_change_redirect': '/'},
    	name='profile'),
]