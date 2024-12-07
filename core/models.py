from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin  
from django.db import models  
import re 

class CustomUserManager(BaseUserManager):  
    def create_user(self, phone_number, email=None, password=None, **extra_fields):  
        if not phone_number:  
            raise ValueError('The Phone Number field must be set')  
        phone_number = self.normalize_phone_number(phone_number)  
        user = self.model(phone_number=phone_number, email=email, **extra_fields)  
        user.set_password(password)  
        user.save(using=self._db)  
        return user  

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):  
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  

        return self.create_user(phone_number, email, password, **extra_fields)  

    def normalize_phone_number(self, phone_number):
        numeric_number = re.sub(r'\D', '', phone_number)  
        last_10_digits = numeric_number[-10:]   
        if len(last_10_digits) == 10:
            normalized_number = '0' + last_10_digits  
            return normalized_number  
        else:  
            return None  

class CustomUser(AbstractBaseUser, PermissionsMixin):  
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='شماره تلفن')  
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True, verbose_name='ایمیل')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')  
    is_staff = models.BooleanField(default=False)  
    mobile_otp = models.CharField(max_length=6, null=True, blank=True, verbose_name='کد تایید شماره تلفن')
    is_mobile_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')
    name = models.CharField(max_length=30, blank=True, verbose_name='نام ')

    USERNAME_FIELD = 'phone_number'  
    REQUIRED_FIELDS = []  

    objects = CustomUserManager()  

    def __str__(self):  
        return self.phone_number 
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'