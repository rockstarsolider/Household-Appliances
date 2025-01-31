from django.shortcuts import render, redirect
from django.views import View
from .models import CartItem, Order
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib import messages  
from .forms import OrderForm
import random

# Create your views here.
@login_required(login_url='/login_phone/')
def cart_summary(request):
    items = CartItem.objects.filter(user=request.user, order__isnull=True)
    # Sum of items in cart, multiplied by their quantity
    total_price = sum((item.product.special_price if item.product.special_price else item.product.price) * item.quantity for item in items) 
    shipment_price = max((item.product.shipment_price for item in items), default=0)
    context = {
        'cart_items': items, 
        'total_price': f'{total_price:,} تومان',
        'shipment_price': f'{shipment_price:,} تومان',
        'final_price': f'{total_price + shipment_price:,} تومان'
    } 
    return render(request, 'dashboard/cart.html', context)

@login_required(login_url='/login_phone/')
def add_to_cart(request, product_id):  
    product = Product.objects.get(id=product_id)  
    cart_item, created = CartItem.objects.get_or_create(  
        product=product,  
        user=request.user,  
        order__isnull=True,
        defaults={'quantity': 1}  
    )  
    if not created:  
        cart_item.quantity += 1  
        cart_item.save()  
    messages.success(request, 'محصول به سبد خرید افزوده شد') 
    return redirect('product', product_id)  

def update_cart(request, item_id):  
    cart_item = CartItem.objects.get(id=item_id)  
    request_quantity = request.GET.get('quantity', cart_item.quantity)
    cart_item.quantity = request_quantity if int(request_quantity) > 0 else 1
    cart_item.save()  
    return redirect('cart')  

def remove_from_cart(request, item_id):  
    cart_item = CartItem.objects.get(id=item_id)  
    cart_item.delete()
    return redirect('cart')

class OrderView(View):
    def get(self, request):
        form = OrderForm() 
        items = CartItem.objects.filter(user=request.user, order__isnull=True)
        total_price = sum((item.product.special_price if item.product.special_price else item.product.price) * item.quantity for item in items) 
        shipment_price = max((item.product.shipment_price for item in items), default=0)
        context = {
            'form': form,
            'total_price': f'{total_price:,} تومان',
            'shipment_price': f'{shipment_price:,} تومان',
            'final_price': f'{total_price + shipment_price:,} تومان'
        }
        return render(request, 'cart/order.html', context)
    
    def post(self, request):
        form = OrderForm(request.POST)  
        items = CartItem.objects.filter(user=request.user, order__isnull=True)
        total_price = sum((item.product.special_price if item.product.special_price else item.product.price) * item.quantity for item in items) 
        shipment_price = max((item.product.shipment_price for item in items), default=0)

        def generate_transaction_id():  
            transaction_id = random.randint(100000, 999999)  
            # Check for uniqueness 
            while Order.objects.filter(transaction_id=transaction_id).exists():  
                transaction_id = random.randint(100000, 999999)  
            return transaction_id

        context = {
            'form': form,
            'total_price': f'{total_price:,} تومان',
            'shipment_price': f'{shipment_price:,} تومان',
            'final_price': f'{total_price + shipment_price:,} تومان'
        }

        if form.is_valid():  
            order = Order.objects.create(
                user = request.user,
                name = request.POST['name'],
                postal_code = request.POST['postal_code'],
                shipping_address = request.POST['shipping_address'],
                total_price = total_price + shipment_price,
                transaction_id = generate_transaction_id()
            )
            items.update(order=order)
            return redirect('transaction_success')
        
        return render(request, 'cart/order.html', context) 
    
class TransactionSuccess(View):
    def get(self, request):
        order = Order.objects.filter(user=request.user).last()
        context = {
            'transaction_id': order.transaction_id,
            'order_id': order.id
        }
        return render(request, 'cart/order_success.html', context)