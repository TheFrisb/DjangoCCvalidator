from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('remove-cart-item/', views.remove_cart_item, name='remove-cart-item'),
    path('update-product-quantity/', views.update_product_quantity, name='update-product-quantity'),
    path('validate-credit-card/', views.validate_credit_card, name='validate-credit-card')
]
