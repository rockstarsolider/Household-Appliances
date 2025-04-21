from django.contrib import admin
from .models import CartItem, Order

# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'product', 'quantity',]
    search_fields = ['user', 'order', 'product', 'quantity',]
    list_filter = ['user', 'order', 'product']
    list_per_page = 50

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'formatted_price', 'order_date', 'transaction_id']
    search_fields = ['user', 'name', 'formatted_price', 'order_date', 'transaction_id']
    list_filter = ['user', 'order_date']
    list_per_page = 50

    @admin.display(description='قیمت کل')  
    def formatted_price(self, obj):  
        return f"{obj.total_price:,} تومان"

admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)