from django.urls import path
from .views import SettingView, OrderListView

urlpatterns = [
    path('setting/', SettingView.as_view(), name= 'setting'),
    path('orders_list/', OrderListView.as_view(), name= 'orders_list'),
]