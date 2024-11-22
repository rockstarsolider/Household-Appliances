from django.db import models 

class Category(models.Model):  
    name = models.CharField(max_length=255, unique=True, verbose_name='نام')  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')  
    
    def __str__(self):  
        return self.name  
    
    class Meta:
        verbose_name_plural = "دسته بندی ها"
        verbose_name = "دسته بندی"
    
class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام'),
    color_code = models.CharField(max_length=10, verbose_name='کد رنگ')

    class Meta:
        verbose_name_plural = "رنگ"
        verbose_name = "رنگ ها"

class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام'),

    class Meta:
        verbose_name_plural = "برند"
        verbose_name = "برند ها"

class Product(models.Model):  
    name = models.CharField(max_length=255, verbose_name='نام')  
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)  
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
    
    class Meta:
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"