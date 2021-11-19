from django.urls import path

from api.order.views import OrderAdd, OrderDetails

app_name = 'order'

urlpatterns = [
    path('add/', OrderAdd.as_view(), name='add'),
    path('update/<int:pk>/', OrderDetails.as_view(), name='update'),
    path('delete/<int:pk>/', OrderDetails.as_view(), name='delete'),
    path('list/<int:pk>/', OrderDetails.as_view(), name='list'),
    path('list/', OrderAdd.as_view(), name='list'),

]