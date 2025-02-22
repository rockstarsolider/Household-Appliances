from django.db import models
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

class WebsiteSetting(models.Model):
    website_name = models.CharField(max_length=50, verbose_name='نام فروشگاه')
    logo = models.ImageField(null=True, blank=True, upload_to='settings/', verbose_name='لوگوی وبسایت')
    banner_1 = models.ImageField(null=True, blank=True, upload_to='settings/', verbose_name='بنر شماره 1')
    banner_2 = models.ImageField(null=True, blank=True, upload_to='settings/', verbose_name='بنر شماره 2')
    banner_3 = models.ImageField(null=True, blank=True, upload_to='settings/', verbose_name='بنر شماره 3')
    phone_number = models.CharField(max_length=12, null=True, blank=True, verbose_name='شماره تلفن')
    telegram_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='آدرس تلگرام')
    instagram_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='آدرس اینستاگرام')
    whatsapp_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='آدرس واتساپ')

    class Meta:
        verbose_name_plural = "تنظیمات"
        verbose_name = "تنظیمات"

    def save(self, *args, **kwargs):
        self.logo = compress(self.logo)
        self.banner_1 = compress(self.banner_1)
        self.banner_2 = compress(self.banner_2)
        self.banner_3 = compress(self.banner_3)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.website_name