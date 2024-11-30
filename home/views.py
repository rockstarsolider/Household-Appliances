from django.shortcuts import render
from django.views import View
from products.models import Product, Category, Brand

# Create your views here.
class HomeView(View):
    def get(self, request):
        latest_products = Product.objects.order_by('-published_at')[:20]
        categories = Category.objects.all()[:20]
        brands = Brand.objects.all()[:20]
        context = {
            'products': latest_products,
            'categories': categories,
            'brands': brands
        }
        return render(request, 'home/home.html', context)