from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserUpdateForm, CustomPasswordForm, PersonalInfoForm
from django.contrib.auth import update_session_auth_hash  
from django.contrib import messages   
from core.models import CustomUser
from cart.models import Order, CartItem
from django.db.models import Sum
from custom_translate.templatetags.persian_calendar_convertor import convert_to_persian_calendar_date, format_persian_date

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
            
class OrderListView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
        # Annotate each order with the total price calculated from its cart items  
        orders = orders.annotate(total_cart_price=Sum('cartitem__quantity') * Sum('cartitem__product__price')).all()
        for order in orders:  
            order.date = format_persian_date(convert_to_persian_calendar_date(order.order_date))
            cart_items = CartItem.objects.filter(order=order)  
            order.products = [{'product_instance': item.product, 'quantity': item.quantity} for item in cart_items] 

        # Retreives all products that user has in his order
        
        context = {
            'orders': orders
        }
        return render(request, 'dashboard/orders_list.html', context)