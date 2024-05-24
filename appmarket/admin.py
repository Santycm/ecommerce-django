from django.contrib import admin

from .models import Carousel,Category, Product, ProductSold
# Register your models here.
admin.site.register(Carousel)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductSold)