from django.urls import path
from api.order_detail.views import OrderDetailadd, OrderDetailDetail

app_name = 'order_detail'

urlpatterns = [
    path('add/', OrderDetailadd.as_view(), name='add'),
    path('update/<int:pk>/', OrderDetailDetail.as_view(), name='update'),
    path('list/<int:pk>/', OrderDetailDetail.as_view(), name='list'),
    path('list/', OrderDetailadd.as_view(), name='list'),

]