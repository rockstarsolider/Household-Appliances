from django.db import models

# Create your models here.
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

    def __str__(self):
        return self.website_name