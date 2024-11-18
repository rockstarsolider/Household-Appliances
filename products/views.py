from django.shortcuts import render
from django.views import View
from django.shortcuts import render

# Create your views here.
class ProductDetailView(View):
    def get(self, request):
        return render(request, 'products/product.html')
    
class ProductListView(View):
    def get(self, request):
        return render(request, 'products/products.html')