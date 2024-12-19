from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import CustomUser
from .utils import generate_otp, verify_otp
from django.views.generic import View
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages
from .forms import PhoneNumberForm, RegisterForm
from threading import Timer  

class PhoneLogin(View):  
    def get(self, request):  
        form = PhoneNumberForm()  
        return render(request, 'core/login_phone.html', {'form': form})  

    def post(self, request):  
        form = PhoneNumberForm(request.POST)  
        if form.is_valid():  
            phone_number = form.cleaned_data['phone_number']  
            try:  
                user = CustomUser.objects.get(phone_number=phone_number)  
                mobile_otp = generate_otp()  
                user.mobile_otp = mobile_otp
                user.otp_generated_at = datetime.now()  
                user.save()  
                print(f"کد تایید شماره تلفن: {mobile_otp}")  
                return redirect('verify_otp', user_id=user.id)  

            except CustomUser.DoesNotExist:  
                otp = generate_otp()
                user = CustomUser.objects.create(  
                    phone_number=phone_number,  
                    is_active=False,
                    mobile_otp = otp,
                    otp_generated_at = datetime.now(),
                )
                print(f"کد تایید شماره تلفن: {otp}")
                Timer(120, self.delete_user, args=[user.id]).start()  
                return redirect('register', id=user.id)  
        else:  
            return render(request, 'core/login_phone.html', {'form': form})
    
    def delete_user(self, user_id):  
        try:  
            user = CustomUser.objects.get(id=user_id)  
            if not user.is_active:
                user.delete()
        except CustomUser.DoesNotExist:  
            pass 

def verify_OTP(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        mobile_otp = request.POST['mobile_otp']

        if verify_otp(mobile_otp, user):
            user.is_mobile_verified = True
            user.mobile_otp = None
            user.save()
            login(request, user)
            messages.success(request, 'کاربر عزیز خوش آمدید')
            return redirect('home')
        else:
            expiration_time = user.otp_generated_at + timedelta(minutes=2)  
            remaining_time = expiration_time - timezone.now()
            context = {
                'number': user.phone_number,
                'expire_time': round(max(remaining_time.total_seconds(), 0)),
                'message': 'کد تایید اشتباه است'
            }
            return render(request, 'core/partial/verify_otp.html', context)

    expiration_time = user.otp_generated_at + timedelta(minutes=2)  
    remaining_time = expiration_time - timezone.now()
    context = {
        'number': user.phone_number,
        'expire_time': round(max(remaining_time.total_seconds(), 0))
    }
    return render(request, 'core/partial/verify_otp.html', context)

class Register(View):
    def get(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
            expiration_time = user.otp_generated_at + timedelta(minutes=2)  
            remaining_time = expiration_time - timezone.now()
            context = {
                'number': user.phone_number,
                'form': RegisterForm(),
                'expire_time': round(max(remaining_time.total_seconds(), 0)),
            }
            return render(request, 'core/partial/register.html', context)
        except CustomUser.DoesNotExist:
            return redirect('login_phone')
        
    def post(self, request, id):
        try:
            form = RegisterForm(request.POST)
            user = CustomUser.objects.get(id=id)
            expiration_time = user.otp_generated_at + timedelta(minutes=2)  
            remaining_time = expiration_time - timezone.now()
            if form.is_valid():  
                otp = form.cleaned_data['otp']  
                name = form.cleaned_data['name'] 
                print(otp)
                if verify_otp(otp, user):
                    user.mobile_otp = None
                    user.is_active=True
                    user.name = name
                    user.save()
                    login(request, user)
                    messages.success(request, 'کاربر عزیز خوش آمدید')
                    return redirect('home') 
                else:
                    context = {
                        'number': user.phone_number,
                        'form': form,
                        'message': 'کد تایید اشتباه است',
                        'expire_time': round(max(remaining_time.total_seconds(), 0)),
                    }
                    return render(request, 'core/partial/register.html', context)
            else:
                return render(request, 'core/partial/register.html', {'form': form}) 
        except CustomUser.DoesNotExist:
            return redirect('login_phone')

class LogoutView(View):  
    def get(self, request, *args, **kwargs):  
        logout(request)
        messages.info(request, 'شما از حساب خود خارج شدید')
        return redirect('home')