from django.db import models
from products.models import Product
from core.models import CustomUser
from django.utils import timezone

# Create your models here.
class Order(models.Model):  
    STATUS_CHOICES = [  
        ('pending', 'پردازش'),  
        ('confirmed', 'ثبت شده'),  
        ('shipped', 'پست شده'), 
        ('cancelled', 'لغو شده'),  
    ]  

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر')  
    name = models.CharField(max_length=70, verbose_name='نام و نام خانوادگی') 
    order_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ سفارش')  
    total_price = models.PositiveBigIntegerField(verbose_name='قیمت کل') 
    shipping_address = models.TextField(verbose_name='آدرس حمل و نقل')  
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')   
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name='شناسه تراکنش')

    def __str__(self):  
        return f"سفارش {self.id} توسط {self.user} - وضعیت: {self.status}"  

    class Meta:  
        verbose_name_plural = "سفارشات"  
        verbose_name = "سفارش" 

class CartItem(models.Model):  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر')  
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, verbose_name='سفارش')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')  

    def __str__(self):  
        return f"{self.product.name} (x{self.quantity})"
    
    class Meta:
        verbose_name_plural = "آیتم سبد خرید"
        verbose_name = "آیتم های سبد خرید"