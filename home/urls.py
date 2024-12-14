from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name= 'home'),
    path('faq/', views.FaqView.as_view(), name= 'faq'),
]