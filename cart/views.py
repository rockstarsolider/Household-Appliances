from django.shortcuts import render, redirect
from django.views import View
from .models import CartItem, Order
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib import messages  
from .forms import OrderForm
import random
from django.db.models import Sum 
from django.db import transaction
from core.sms import send_order_sms_threaded

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
    return render(request, 'products/partial/added_to_card_btn.html')

def update_cart(request, item_id):  
    cart_item = CartItem.objects.get(id=item_id)  
    request_quantity = request.GET.get('quantity', cart_item.quantity)
    if int(request_quantity) > cart_item.product.stock:
        messages.error(request, "محصول انتخاب شده به اندازه کافی موجود نیست")  
        return redirect('cart') 
    cart_item.quantity = request_quantity if int(request_quantity) > 0 else 1
    cart_item.save()  
    return redirect('cart')  

def remove_from_cart(request, item_id):  
    cart_item = CartItem.objects.get(id=item_id)  
    cart_item.delete()
    return redirect('cart')

class OrderView(View):
    def get(self, request):
        form = OrderForm(initial={
                'shipping_address': request.user.shipment_address,
                'postal_code': request.user.postal_code,
                'name': request.user.name
            }) 
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
            # Updates the number of sales and reduce the quantity of each product ordered
            cart_items = items.values('product').annotate(total_quantity=Sum('quantity'))   
            products_to_update = []  
            insufficient_stock_items = []  

            try:  
                with transaction.atomic():  
                    for item in cart_items:  
                        product = Product.objects.get(id=item['product'])  
                        total_quantity = item['total_quantity']  

                        # Check if there is enough stock available  
                        if total_quantity > product.stock:  
                            insufficient_stock_items.append(product.name)  
                            continue  

                        # Prepare updates for bulk processing  
                        product.number_of_sales += total_quantity  
                        product.stock -= total_quantity  # Update the stock instead of quantity  
                        products_to_update.append(product)  

                    # Perform bulk update if there are products to update  
                    if products_to_update:  
                        Product.objects.bulk_update(products_to_update, ['number_of_sales', 'stock'])  

            except Product.DoesNotExist:  
                messages.error(request, "Some products no longer exist.")  
                return redirect('cart')  

            if insufficient_stock_items:  
                for product_name in insufficient_stock_items:  
                    messages.error(request, f'محصول {product_name} به اندازه کافی موجود نیست')  
                return redirect('cart')

            order = Order.objects.create(
                user = request.user,
                name = request.POST['name'],
                postal_code = request.POST['postal_code'],
                shipping_address = request.POST['shipping_address'],
                total_price = total_price + shipment_price,
                transaction_id = generate_transaction_id(),
                status = 'cancelled'
            )
            items.update(order=order)
            return redirect('transaction_success')
        
        return render(request, 'cart/order.html', context) 
    
class TransactionSuccess(View):
    def get(self, request):
        order = Order.objects.filter(user=request.user).last()
        order.status = 'pending'
        order.save()

        # Sending sms for user
        send_order_sms_threaded(order.user.phone_number, order.pk)

        context = {
            'transaction_id': order.transaction_id,
            'order_id': order.pk
        }
        return render(request, 'cart/order_success.html', context)