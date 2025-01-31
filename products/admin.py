from django.contrib import admin
from .models import Product, Category, Brand, ProductImage, Comment
from django.utils.html import format_html

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    readonly_fields = ('image_preview',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user']

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['image_tag', 'id', 'name', 'category', 'formatted_price', 'formatted_special_price', 'stock', 'published_at']
    search_fields = ['name', 'id']
    list_display_links = ['name', 'image_tag']
    list_per_page = 50

    @admin.display(description='قیمت')  
    def formatted_price(self, obj):  
        return obj.formatted_price
    
    @admin.display(description='قیمت ویژه')  
    def formatted_special_price(self, obj):  
        return obj.formatted_special_price

    @admin.display(description='تصویر')  
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:64px; max-height:64px"/>'.format(obj.image.url))
    
    def save_model(self, request, obj, form, change):  
        obj.clean()  # Call the clean method  
        super().save_model(request, obj, form, change) 

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Comment, CommentAdmin)