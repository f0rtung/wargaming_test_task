from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^server/', include('serverapp.urls')),
    url(r'^admin/', admin.site.urls),
]
