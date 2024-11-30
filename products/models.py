from django.db import models 
from django_ckeditor_5.fields import CKEditor5Field  
from django.utils.safestring import mark_safe

class Category(models.Model):  
    name = models.CharField(max_length=255, unique=True, verbose_name='نام') 
    image = models.ImageField(upload_to='categories/', default='default.png', verbose_name='تصویر دسته بندی')  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')  
    
    def __str__(self):  
        return self.name  
    
    class Meta:
        verbose_name_plural = "دسته بندی ها"
        verbose_name = "دسته بندی"
        ordering = ["-created_at"]
    
class Color(models.Model):
    title = models.CharField(max_length=255, verbose_name='نام')
    color_code = models.CharField(max_length=10, verbose_name='کد رنگ')

    class Meta:
        verbose_name_plural = "رنگ"
        verbose_name = "رنگ ها"
    def __str__(self):  
        return self.title

class Brand(models.Model):
    title = models.CharField(max_length=255, verbose_name='نام')
    image = models.ImageField(upload_to='brands/', default='default.png', verbose_name='تصویر برند')  

    class Meta:
        verbose_name_plural = "برند"
        verbose_name = "برند ها"
    def __str__(self):  
        return self.title

class Product(models.Model):  
    name = models.CharField(max_length=255, verbose_name='نام')  
    description = CKEditor5Field(verbose_name='توضیحات', null=True, blank=True, config_name='extends')  
    price = models.PositiveBigIntegerField(verbose_name='قیمت') 
    special_price = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='قیمت ویژه') 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='دسته بندی')  
    image = models.ImageField(upload_to='products/', default='default.png', verbose_name='تصویر اصلی')  
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')  
    published_at = models.DateTimeField(verbose_name='منتشر شده در')
    portable = models.BooleanField(blank=True, null=True, verbose_name='قابلیت حمل')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='رنگ')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='برند')

    def __str__(self):  
        return self.name  

    def is_in_stock(self):  
        return self.stock > 0  
    
    def formatted_price(self):
        return f"{self.price:,} تومان"
    
    class Meta:
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='تصویر ') 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول مرتبط')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='آپلود شده در')

    def image_preview(self):
        return mark_safe('<img src="{0}" width="64" height="64" />'.format(self.image.url))

    class Meta:
        verbose_name_plural = "تصویر"
        verbose_name = "تصاویر"