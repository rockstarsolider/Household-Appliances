from django.contrib import admin
from .models import Product, Category, Brand, Color, ProductImage

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(ProductImage)