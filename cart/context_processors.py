from .models import CartItem

def cart_items_number(request):
    return {'cart_items_number': CartItem.objects.filter(user=request.user).count()}