from django.db import models 

class Category(models.Model):  
    name = models.CharField(max_length=255, unique=True, verbose_name='نام')  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')  
    
    def __str__(self):  
        return self.name  
    
    class Meta:
        verbose_name_plural = "دسته بندی ها"
        verbose_name = "دسته بندی"

class Product(models.Model):  
    name = models.CharField(max_length=255, verbose_name='نام')  
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)  
    price = models.PositiveBigIntegerField(verbose_name='قیمت') 
    special_price = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='قیمت ویژه') 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='دسته بندی')  
    image = models.ImageField(upload_to='products/', default='default.png', verbose_name='تصویر اصلی')  
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')  
    published_at = models.DateTimeField(verbose_name='منتشر شده در')
    properties = models.TextField(blank=True, verbose_name='ویژگی ها', help_text="Enter properties in the format 'key: value' on separate lines.")

    def __str__(self):  
        return self.name  

    def is_in_stock(self):  
        return self.stock > 0  
    
    def properties_dict(self):  
        properties_dict = {}  
        for line in self.properties.splitlines():  
            if ':' in line:  
                key, value = line.split(':', 1)  
                properties_dict[key.strip()] = value.strip()  
        return properties_dict 
    
    class Meta:
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"