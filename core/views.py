from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import CustomUser
from .utils import generate_otp, verify_otp
from django.views.generic import View

class PhoneLogin(View):
    def get(self, request):
        return render(request, 'core/login_phone.html')
    
    def post(self, request):
        phone_number = request.POST['phone_number']
        try:  
            user = CustomUser.objects.get(phone_number=phone_number)  
            
            # Generate and save OTPs for the existing user  
            mobile_otp = generate_otp()
            user.mobile_otp = mobile_otp
            user.save()
            
            # Send mobile OTP (for now just printing)  
            print(f"کد تایید شماره تلفن: {mobile_otp}")  

            # Redirect to verify OTP  
            return redirect('verify_otp', user_id=user.id)
        
        except CustomUser.DoesNotExist:   
            return redirect('register', number=phone_number)

def verify_OTP(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        mobile_otp = request.POST['mobile_otp']

        if verify_otp(mobile_otp, user.mobile_otp):
            user.is_mobile_verified = True
            user.mobile_otp = None
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'core/partial/verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'core/partial/verify_otp.html', {'number': user.phone_number})

class Register(View):
    def get(self, request, number):
        return render(request, 'core/partial/register.html', {'number': number})

class LogoutView(View):  
    def get(self, request, *args, **kwargs):  
        logout(request)
        return redirect('home')