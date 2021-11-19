from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include

urlpatterns = [
    url(r"api", include("api.urls"), name="api"),
    path('admin/', admin.site.urls),
]