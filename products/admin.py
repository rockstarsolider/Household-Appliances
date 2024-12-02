from django.contrib import admin
from .models import Product, Category, Brand, Color, ProductImage
from django.utils.html import format_html

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    readonly_fields = ('image_preview',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['image_tag', 'id', 'name', 'category', 'formatted_price', 'special_price', 'stock', 'published_at']
    search_fields = ['name', 'id']
    list_display_links = ['name', 'image_tag']
    list_per_page = 50
    ordering = ['published_at']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:40px; max-height:40px"/>'.format(obj.image.url))
    
    def save_model(self, request, obj, form, change):  
        obj.clean()  # Call the clean method  
        super().save_model(request, obj, form, change) 

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Color)