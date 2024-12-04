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
        selected_portable = request.GET.get('portable')
        selected_discount = request.GET.get('discount')
        selected_stock = request.GET.get('stock')
        selected_from = request.GET.get('from')
        selected_to = request.GET.get('to')
        selected_order = request.GET.get('order')
        
        if selected_category: products = products.filter(category=selected_category)
        if selected_brand: products = products.filter(brand=selected_brand)
        if selected_portable == 'true': products = products.filter(portable=True)
        if selected_discount == 'true': products = products.filter(special_price__isnull=False)
        if selected_stock == 'true': products = products.filter(stock__gt=0)
        if selected_from: products = products.filter(price__gte=selected_from)
        if selected_to: products = products.filter(price__lte=selected_to)
        if selected_order == 'cheapest': products = products.order_by('-price')
        if selected_order == 'expensive': products = products.order_by('price')

        context = {
            'products': products,
            'brands': Brand.objects.all(),
            'categories': Category.objects.all(),

            'selected_category': selected_category,
            'selected_brand': selected_brand,
            'selected_portable': selected_portable,
            'selected_discount': selected_discount,
            'selected_stock': selected_stock,
            'selected_from': selected_from,
            'selected_to': selected_to,
            'selected_order': selected_order,
            'order': selected_order
        }

        return render(request, 'products/products.html', context)