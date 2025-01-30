from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_summary, name= 'cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),  
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'), 
]