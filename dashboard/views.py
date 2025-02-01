from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserUpdateForm, CustomPasswordForm, PersonalInfoForm
from django.contrib.auth import update_session_auth_hash  
from django.contrib import messages   
from core.models import CustomUser

# Create your views here.
class SettingView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = CustomUserUpdateForm(instance=request.user)  
        password_form = CustomPasswordForm()
        context = {  
            'user_form': user_form,  
            'password_form': password_form,  
            'personal_form': PersonalInfoForm()
        }  
        return render(request, 'dashboard/setting.html', context)
    
    def post(self, request):
        post_type = request.GET.get('type')
        if post_type == 'account':
            user_form = CustomUserUpdateForm(request.POST, instance=request.user)  
            password_form = CustomPasswordForm(request.POST) 
            context = {  
                'user_form': user_form,  
                'password_form': password_form,  
                'personal_form': PersonalInfoForm()
            }
            
            if user_form.is_valid() and password_form.is_valid():  
                user_form.save()  # Update the email  
                password = password_form.cleaned_data['password1']  
                request.user.set_password(password)  
                request.user.save()
                update_session_auth_hash(request, request.user)

                messages.success(request, 'پروفایل شما با موفقیت تغییر یافت')  
                return render(request, 'dashboard/setting.html', context)
            else:
                return render(request, 'dashboard/setting.html', context)
        elif post_type == 'personal':
            personal_form = PersonalInfoForm(request.POST) 
            context = {  
                'user_form': CustomUserUpdateForm( instance=request.user),  
                'password_form': CustomPasswordForm(),  
                'personal_form': PersonalInfoForm(request.POST)
            }
            if personal_form.is_valid():
                user = CustomUser.objects.get(pk=request.user.pk)
                user.name = personal_form.clean_name()
                user.postal_code = personal_form.clean_postal_code()
                user.shipment_address = personal_form.clean_shipping_address()
                user.save()

                messages.success(request, 'پروفایل شما با موفقیت تغییر یافت')  
                return render(request, 'dashboard/setting.html', context)
            else:
                return render(request, 'dashboard/setting.html', context)