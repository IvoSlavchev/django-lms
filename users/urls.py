from django.conf.urls import url

from users import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^confirm$', views.confirm, name='confirm'),
    url(r'^logout$', views.logout, name='logout'),
]