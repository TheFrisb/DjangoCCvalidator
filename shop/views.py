from django.shortcuts import render
from django.core.paginator import Paginator
from shop.models import Product
# Create your views here.


def index(request):
    products_all = Product.objects.filter(status='PUBLISHED')
    paginator = Paginator(products_all, 16) # 16 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'is_paginated': True,
        'products': products,
        'title': 'Shop'
    }
    return render(request, 'shop/shop_home.html', context=context)
    
