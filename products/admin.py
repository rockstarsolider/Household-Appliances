from django.contrib import admin
from .models import Product, Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)