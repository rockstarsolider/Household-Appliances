from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Product, ProductImage, Category, Brand

# Create your views here.
class ProductDetailView(DetailView):  
    model = Product  
    template_name = 'products/product.html'  
    context_object_name = 'product'  
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['images'] = ProductImage.objects.filter(product=self.object)  
        context['products'] = Product.objects.filter(category=self.object.category)
        return context  

class ProductListView(View):
    def get(self, request):
        products = Product.objects.order_by('published_at')

        selected_category = request.GET.get('category')
        selected_brand = request.GET.get('brand')
        
        if selected_category:
            products = products.filter(category=selected_category)
        if selected_brand:
            products = products.filter(brand=selected_brand)

        context = {
            'products': products,
            'brands': Brand.objects.all(),
            'categories': Category.objects.all(),

            'selected_category': selected_category,
            'selected_brand': selected_brand,
        }

        return render(request, 'products/products.html', context)