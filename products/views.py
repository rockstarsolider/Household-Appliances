from django.shortcuts import render
from django.views import View
from django.shortcuts import render
from .models import Product, ProductImage

# Create your views here.
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        images = ProductImage.objects.filter(product=product)
        context = {
            'product': product,
            'images': images
        }
        return render(request, 'products/product.html', context)
    
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products/products.html', {'products': products})