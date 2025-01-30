from django.db import models
from products.models import Product
from core.models import CustomUser

# Create your models here.
class CartItem(models.Model):  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر')  
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')  

    def __str__(self):  
        return f"{self.product.name} (x{self.quantity})"
    
    class Meta:
        verbose_name_plural = "آیتم سبد خرید"
        verbose_name = "آیتم های سبد خرید"