from django.urls import path

from api.product.views import ProductAdd, ProductDetail
from . import views

app_name = 'product'

urlpatterns = [
    path('add/', ProductAdd.as_view(), name='add'),
    path('update/<int:pk>/', ProductDetail.as_view(), name='update'),
    path('delete/<int:pk>/', ProductDetail.as_view(), name='delete'),
    path('list/', ProductAdd.as_view(), name='list'),

]