from django.contrib import admin

from .models import Carousel, Users, Category, Product, ProductSold
# Register your models here.
admin.site.register(Carousel)
admin.site.register(Users)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductSold)