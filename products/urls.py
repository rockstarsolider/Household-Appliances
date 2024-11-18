from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductDetailView.as_view()),
    path('products/', views.ProductListView.as_view()),
]