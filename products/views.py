from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Product, ProductImage, Category, Brand, Comment
from .forms import CommentForm
from django.contrib import messages
from django.db.models import Case, When, IntegerField  
from django.core.paginator import Paginator

# Create your views here.
class ProductDetailView(DetailView):  
    model = Product  
    template_name = 'products/product.html'  
    context_object_name = 'product'  
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['images'] = ProductImage.objects.filter(product=self.object)  
        context['products'] = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)
        context['comments'] = Comment.objects.filter(product=self.object.id)
        context['form'] = CommentForm()
        return context 
    
    def post(self, request, pk):  
        form = CommentForm(request.POST)
        product = Product.objects.get(pk=pk)
        comments = Comment.objects.filter(product=product)
        
        if form.is_valid():
            text = form.cleaned_data['text']
            comment = Comment(
                user=request.user,
                product=product,
                text=text
            )
            comment.save()
            context = {
                'comments':comments,
                'form': CommentForm(),
                'product': product,
            }
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
            return render(request, 'products/partial/comments.html', context)

        context = {
            'comments':comments,
            'form': form,
            'product': product,
        }
        return render(request, 'products/partial/comments.html', context)

class ProductListView(View):
    def get(self, request):
        products = Product.objects.annotate(  
            in_stock_order=Case(  
                When(stock__gt=0, then=0),   # If stock is greater than 0, assign order 0  
                When(stock=0, then=1),       # If stock is 0, assign order 1  
                output_field=IntegerField()   # Specify output field type  
            )  
        ).order_by('in_stock_order', '-published_at')

        selected_category = request.GET.get('category')
        selected_brand = request.GET.get('brand')
        selected_discount = request.GET.get('discount')
        selected_stock = request.GET.get('stock')
        selected_from = request.GET.get('from')
        selected_to = request.GET.get('to')
        selected_order = request.GET.get('order')
        search = request.GET.get('search')
        
        if selected_category: products = products.filter(category=selected_category)
        if selected_brand: products = products.filter(brand=selected_brand)
        if selected_discount == 'true': products = products.filter(special_price__isnull=False, stock__gt=0)
        if selected_stock == 'true': products = products.filter(stock__gt=0)
        if selected_from: products = products.filter(price__gte=selected_from)
        if selected_to: products = products.filter(price__lte=selected_to)
        if selected_order == 'cheapest': products = products.order_by('in_stock_order', 'price')
        if selected_order == 'expensive': products = products.order_by('in_stock_order', '-price')
        if selected_order == 'popular': products = products.order_by('in_stock_order', '-number_of_sales')
        if search: products = products.filter(name__contains=search)

        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'products': page_obj.object_list,
            'brands': Brand.objects.all(),
            'categories': Category.objects.all(),

            'selected_category': selected_category,
            'selected_brand': selected_brand,
            'selected_discount': selected_discount,
            'selected_stock': selected_stock,
            'selected_from': selected_from,
            'selected_to': selected_to,
            'selected_order': selected_order,
            'order': selected_order
        }

        return render(request, 'products/products.html', context)