from django.contrib import admin
from .models import *


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['status']
    list_display = ("title", "price",  "created_at")

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)