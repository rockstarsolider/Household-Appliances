from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'name', 'email',]
    search_fields = ['phone_number', 'id', 'name', 'email',]
    list_display_links = ['phone_number']
    list_filter = ['is_staff', 'date_joined']
    list_per_page = 50

admin.site.register(CustomUser, CustomUserAdmin)