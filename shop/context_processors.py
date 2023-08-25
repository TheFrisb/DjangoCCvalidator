from .models import Cart, CartItem
import uuid

def load_shop_context(request):
    try:
        cart = Cart.objects.get(session=request.session['anonymousUser'])
    except:
        request.session['anonymousUser'] = str(uuid.uuid4())
        cart = Cart.objects.create(session=request.session['anonymousUser'])
    
    cart_items = cart.cartitem_set.all().prefetch_related('product') 
    
    return {'cart': cart, 'cart_items': cart_items}