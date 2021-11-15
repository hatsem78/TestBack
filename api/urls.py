# coding=utf-8
from django.urls import path

from django.conf.urls import url, include
from rest_framework import routers



router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),

    path('/user/', include('api.user.urls')),
    path('api-auth/', include('rest_framework.urls')),

]
