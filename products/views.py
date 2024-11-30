from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductImage

# Create your views here.
class ProductDetailView(DetailView):  
    model = Product  
    template_name = 'products/product.html'  
    context_object_name = 'product'  
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['images'] = ProductImage.objects.filter(product=self.object)  
        return context  
    
class ProductListView(ListView):
    model = Product 
    template_name = 'products/products.html'  
    context_object_name = 'products'  # default is 'object_list'  
    paginate_by = 30

    def get_queryset(self):  
        return Product.objects.order_by('published_at')