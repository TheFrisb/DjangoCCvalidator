from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from shop.models import *
from . import helpers
import datetime

# Create your views here.
def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'success': False,'message': 'Invalid method'}, status=400)
    
    try:
        cart = Cart.objects.get(session=request.session['anonymousUser'])
    except Cart.DoesNotExist:
        return JsonResponse({'success': False,'message': 'Cart not found!'}, status=400)
    
    product_id = request.POST.get('productId')
    if product_id is not None and product_id.isdigit():
        try:
            product = Product.objects.get(id=int(product_id))
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found!'})
        
        cart_item = CartItem.objects.filter(product=product).first()
        
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
                    
            cart.total_price += product.price
            cart.save()
            responseProduct = {
                        'id': product.id,
                        'title': product.title,
                        'thumbnail': product.thumbnail.url,
                        'sale_price': product.price,
                        'currentQuantity': cart_item.quantity,
                    }
                    
            return JsonResponse({
                'success': True,
                'message': 'Product is in cart, and quantity updated!',
                'inCart': True,
                'currentQty': cart_item.quantity,
                'product': responseProduct,
                'cartTotal': cart.total_price,
                'totalItems': cart.number_of_items,
            }, status=200)
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=1)
            cart.total_price += product.price
            cart.number_of_items +=1
            
            cart.save()
            responseProduct = {
                        'id': product.id,
                        'title': product.title,
                        'thumbnail': product.thumbnail.url,
                        'sale_price': product.price,
                        'currentQuantity': 1,
            }

        return JsonResponse({
                    'success': True,
                    'message': 'Product added to cart!',
                    'inCart': False,
                    'product': responseProduct,
                    'cartTotal': cart.total_price,
                    'totalItems': cart.number_of_items,
                }, status=201)
    else:
        return JsonResponse({'success': False,'message': 'Invalid parameters'}, status=400)


def remove_cart_item(request):
    if request.method != 'POST':
        return JsonResponse({'success': False,'message': 'Invalid method'}, status=400)
    
    product_id = request.POST.get('productId')
    if product_id is not None and product_id.isdigit():
        try:
            cart = Cart.objects.get(session=request.session['anonymousUser'])
        except Cart.DoesNotExist:
            return JsonResponse({'success': False,'message': 'Cart not found!'}, status=400)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product__id=int(product_id))
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False,'message': 'Product is not in cart!'}, status=400)
        product = cart_item.product
        cart.total_price -= cart_item.product.price * cart_item.quantity
        cart.number_of_items -= 1
        cart.save()
        cart_item.delete()
        
        responseProduct = {
                    'id': product.id,
                    'title': product.title,
                    'thumbnail': product.thumbnail.url,
                    'sale_price': product.price,
                    'currentQuantity': 0,
        }
        
        return JsonResponse({
                    'success': True,
                    'message': 'Product removed!',
                    'inCart': False,
                    'product': responseProduct,
                    'cartTotal': cart.total_price,
                    'totalItems': cart.number_of_items,
                }, status=201)
        
    else:
        return JsonResponse({'success': False,'message': 'Invalid parameters'}, status=400)
    

def update_product_quantity(request):
    if request.method != 'POST':
        return JsonResponse({'success': False,'message': 'Invalid method'}, status=400)
    product_id = request.POST.get('productId')
    quantity = request.POST.get('quantity')
    if product_id is not None and product_id.isdigit() and quantity is not None and quantity.isdigit():
        new_quantity = int(quantity)
        try:
            cart = Cart.objects.get(session=request.session['anonymousUser'])
        except Cart.DoesNotExist:
            return JsonResponse({'success': False,'message': 'Cart not found!'}, status=400)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product__id=int(product_id))
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False,'message': 'Product is not in cart!'}, status=400)
        
        product = cart_item.product
        current_quantity = cart_item.quantity
        if new_quantity > 0:
            
            if current_quantity > new_quantity:
                cart.total_price -= product.price * (current_quantity - new_quantity)
            else:
                cart.total_price += product.price * (new_quantity - current_quantity)
            
            cart_item.quantity = new_quantity
            cart_item.save()
            cart.save()
            responseProduct = {
                    'id': product.id,
                    'title': product.title,
                    'thumbnail': product.thumbnail.url,
                    'sale_price': product.price,
                    'currentQuantity': cart_item.quantity,
            }
            
            return JsonResponse({
                    'success': True,
                    'message': 'Product quantity updated, still in cart!',
                    'inCart': True,
                    'product': responseProduct,
                    'cartTotal': cart.total_price,
                    'totalItems': cart.number_of_items,
                }, status=200)
        else:
            cart.total_price -= product.price * current_quantity
            cart.number_of_items -= 1
            cart.save()
            cart_item.delete()
            responseProduct = {
                    'id': product.id,
                    'title': product.title,
                    'thumbnail': product.thumbnail.url,
                    'sale_price': product.price,
                    'currentQuantity': 0,
            }
            
            return JsonResponse({
                    'success': True,
                    'message': 'Product quantity updated, removed from cart!',
                    'inCart': False,
                    'product': responseProduct,
                    'cartTotal': cart.total_price,
                    'totalItems': cart.number_of_items,
                }, status=200)
            
    else:
        return JsonResponse({'success': False,'message': 'Invalid parameters'}, status=400)
    

def validate_credit_card(request):
    if request.method != 'POST':
        return JsonResponse({'success': False,'message': 'Invalid method'}, status=400)
    
    errors = []
    card_number = request.POST.get('cardNumber')
    valid_through = request.POST.get('validThrough')
    cvv = request.POST.get('CVV')
    
    if card_number is None or card_number == "":
        errors.append('Please fill the card number input')
    
    
    if valid_through is None or valid_through == "":
        errors.append('Please fill the valid through input')

    
    if len(valid_through) != 5 or '/' not in valid_through:
        errors.append('Please enter valid through as example: 06/25 (month, year)')
        
    if cvv is None or cvv == "":
        errors.append('Please fill the CVV input')

    
    if errors:
        return JsonResponse({'success': False, 'message': 'Missing fields', 'errors': errors}, status=400)
    
    

    try:
        month,year = valid_through.split('/')
        expiry_date= datetime.datetime(int('20' + year), int(month), 1)
        if expiry_date <= datetime.datetime.now():
            return JsonResponse({'success': False, 'message': 'Invalid expiry date'}, status=400)
    except (ValueError, IndexError):
        print(expiry_date)
        return JsonResponse({'success': False, 'message': 'Invalid date format'}, status=400)
    card_type = helpers.get_card_type(card_number)
    if card_type == 'American Express':
        if len(cvv) != 4:
            return JsonResponse({'success': False, 'message': 'CVV must be 4 digits for American Express!'}, status=400)
    else:
        if len(cvv)  != 3:
            return JsonResponse({'success': False, 'message': 'CVV must be 3 digits for your card type!'}, status=400)
    
    if not helpers.is_valid_pan_length(card_number):
        return JsonResponse({'success': False, 'message': 'Credit card length must be between 16 and 19 digits long'}, status=400)
    
    if not helpers.is_valid_pan_luhn(card_number):
        return JsonResponse({'success': False, 'message': 'Invalid credit card'}, status=400)

    return JsonResponse({'success': True, 'message': 'Credit card is valid'}, status=200)