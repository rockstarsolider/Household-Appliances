from django.shortcuts import render
from django.views import View
from products.models import Product, Category, Brand

# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        latest_products = products.order_by('-published_at')[:20]
        populars = products.order_by('-number_of_sales')[:20]
        categories = Category.objects.all()[:20]
        brands = Brand.objects.all()[:20]
        context = {
            'products': latest_products,
            'categories': categories,
            'brands': brands,
            'populars': populars
        }
        return render(request, 'home/home.html', context)
    
class FaqView(View):
    def get(self, request):
        return render(request, 'home/questions.html')