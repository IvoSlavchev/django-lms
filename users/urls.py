from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^teacher_page.html$', views.teacher_page, name='teacher_page'),
    url(r'^student_page.html$', views.student_page, name='student_page'),
]
