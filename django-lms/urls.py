from django.conf.urls import include, url
from django.contrib import admin

from users import urls as users_urls
from teachers import urls as teachers_urls
from students import urls as students_urls

urlpatterns = [
	url(r'^', include(users_urls)),
	url(r'^teachers/', include(teachers_urls)),
	url(r'^students/', include(students_urls)),
	#url(r'^admin/', include(admin.site.urls)),
]