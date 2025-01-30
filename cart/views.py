from django.shortcuts import render, redirect
from .models import CartItem
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib import messages  

# Create your views here.
@login_required(login_url='/login_phone/')
def cart_summary(request):
    items = CartItem.objects.filter(user=request.user)  
    # Sum of items in cart, multiplied by their quantity
    total_price = sum((item.product.special_price if item.product.special_price else item.product.price) * item.quantity for item in items) 
    shipment_price = 45000
    context = {
        'cart_items': items, 
        'total_price': f'{total_price:,} تومان',
        'shipment_price': f'{shipment_price:,} تومان',
        'final_price': f'{total_price + shipment_price:,} تومان'
    } 
    return render(request, 'dashboard/cart.html', context)

def add_to_cart(request, product_id):  
    product = Product.objects.get(id=product_id)  
    cart_item, created = CartItem.objects.get_or_create(  
        product=product,  
        user=request.user,  
        defaults={'quantity': 1}  
    )  
    if not created:  
        cart_item.quantity += 1  
        cart_item.save()  
    messages.success(request, 'محصول به سبد خرید افزوده شد') 
    return redirect('product', product_id)  

def update_cart(request, item_id):  
    cart_item = CartItem.objects.get(id=item_id)  
    cart_item.quantity = request.GET.get('quantity', cart_item.quantity)  
    cart_item.save()  
    return redirect('cart')  

def remove_from_cart(request, item_id):  
    cart_item = CartItem.objects.get(id=item_id)  
    cart_item.delete()
    messages.warning(request, 'محصول با موفقیت حذف شد') 
    return redirect('cart')