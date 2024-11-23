from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name= 'product'),
    path('products/', views.ProductListView.as_view(), name= 'products'),
]