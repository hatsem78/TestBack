# coding=utf-8
from django.urls import path

from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),

    path('user', include('api.user.urls')),
    path('/product/', include('api.product.urls')),
    path('/order/', include('api.order.urls')),
    path('/order_detail/', include('api.order_detail.urls')),

    path('api-auth/', include('rest_framework.urls')),

]
