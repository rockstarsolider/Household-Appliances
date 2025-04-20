from django.db import models 
from django_ckeditor_5.fields import CKEditor5Field  
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from core.models import CustomUser  
from io import BytesIO
from PIL import Image
from django.core.files import File

def compress(image):  
    img = Image.open(image)  
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):  
        background = Image.new('RGB', img.size, (255, 255, 255))  
        if img.mode == 'RGBA':  
            background.paste(img, (0, 0), img.split()[3])
        elif img.mode == 'LA':  
            background.paste(img, (0, 0), img.split()[1])
        elif img.mode == 'P':  
            img = img.convert('RGBA')  
            background.paste(img, (0, 0), img.split()[3])
        img = background 
    elif img.mode == 'P':  
        img = img.convert('RGB')  
    img_io = BytesIO()  
    img.save(img_io, 'JPEG', quality=60)  
    new_image = File(img_io, name=image.name.split('.')[0] + '.jpg')  
    return new_image

class Category(models.Model):  
    name = models.CharField(max_length=255, unique=True, verbose_name='نام') 
    image = models.ImageField(upload_to='categories/', default='default.png', verbose_name='تصویر دسته بندی')  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')  
    
    def __str__(self):  
        return self.name  
    
    def save(self, *args, **kwargs):
        self.image = compress(self.image)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "دسته بندی ها"
        verbose_name = "دسته بندی"
        ordering = ["-created_at"]

class Brand(models.Model):
    title = models.CharField(max_length=255, verbose_name='نام')
    image = models.ImageField(upload_to='brands/', default='default.png', verbose_name='تصویر برند')  

    class Meta:
        verbose_name_plural = "برند"
        verbose_name = "برند ها"

    def save(self, *args, **kwargs):
        self.image = compress(self.image)
        super().save(*args, **kwargs)

    def __str__(self):  
        return self.title

class Product(models.Model): 
    UNIT_CHOICES = [  
        ('int', 'عدد'),  
        ('box', 'جعبه'),  
        ('dozen', 'جین'),
    ]

    name = models.CharField(max_length=255, verbose_name='نام')  
    short_description = models.CharField(max_length=60, null=True, blank=True, verbose_name='توضیحات کوتاه')  
    description = CKEditor5Field(verbose_name='توضیحات', null=True, blank=True, config_name='extends')  
    price = models.PositiveBigIntegerField(verbose_name='قیمت') 
    special_price = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='قیمت ویژه') 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='دسته بندی')  
    image = models.ImageField(upload_to='products/', default='default.png', verbose_name='تصویر اصلی')  
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')  
    published_at = models.DateTimeField(verbose_name='منتشر شده در')
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES, default='int', verbose_name='واحد')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='برند')
    shipment_price = models.PositiveBigIntegerField(default=45000 ,verbose_name='هزینه پست') 
    number_of_sales = models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')

    def __str__(self):  
        return self.name 

    def save(self, *args, **kwargs):
        self.image = compress(self.image)
        super().save(*args, **kwargs) 

    @property
    def is_in_stock(self):  
        return self.stock > 0  
    
    @property
    def formatted_price(self):
        return f"{self.price:,} تومان"
    
    @property
    def formatted_special_price(self):
        if self.special_price:
            return f"{self.special_price:,} تومان"
        
    def clean(self):  
        if self.special_price is not None and self.special_price >= self.price:  
            raise ValidationError('قیمت ویژه باید کمتر از قیمت باشد.')  
    
    class Meta:
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"
        ordering = ['-published_at']

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='تصویر ') 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول مرتبط')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='آپلود شده در')

    def image_preview(self):
        return mark_safe('<img src="{0}" width="64" height="64" />'.format(self.image.url))
    
    def save(self, *args, **kwargs):
        self.image = compress(self.image)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "تصویر"
        verbose_name = "تصاویر"

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالای مرتبط')
    text = models.TextField(max_length=300, verbose_name='متن')

    class Meta:
        verbose_name_plural = "دیدگاه"
        verbose_name = "دیدگاه ها"