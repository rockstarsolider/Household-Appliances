from django.urls import path
from core import views

urlpatterns = [
    path('login_phone/', views.PhoneLogin.as_view(), name='login_phone'),
    path('verify_otp/<int:user_id>/', views.verify_OTP, name='verify_otp'),
    path('register/<int:id>/', views.Register.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]