from .models import CartItem

def cart_items_number(request):
    if request.user.is_authenticated:
        number = CartItem.objects.filter(user=request.user, order__isnull=True).count()
    else:
        number = 0
    return {'cart_items_number': number}