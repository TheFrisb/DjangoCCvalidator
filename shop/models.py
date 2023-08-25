from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

# Create your models here.
class Product(models.Model):
    status_choices = (
        ('PRIVATE', 'PRIVATE'),
        ('PUBLISHED', 'PUBLISHED'),
    )
    status = models.CharField(choices = status_choices, default = 'PRIVATE', max_length=20)
    title = models.CharField(max_length = 100)
    thumbnail = ProcessedImageField(upload_to='products/thumbnails/%Y/%m/%d/', processors=[ResizeToFill(550,550)], format='WEBP', options={'quality': 95}, verbose_name='Thumbnail', null=True)
    thumbnail_as_png = ImageSpecField(source='thumbnail',format='PNG')
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    
class Cart(models.Model):
    session = models.CharField(max_length=100)
    total_price = models.IntegerField(default=0)
    number_of_items = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return '{} - {}'.format(self.session, self.created_at)
    
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return 'Cart item ({product_title}) for Cart session ID {cart_session_id}'.format(product_title=self.product.title, cart_session_id=self.cart.session)
    
    
    class Meta:
        verbose_name = 'Cart item'
        verbose_name_plural = 'Cart items'