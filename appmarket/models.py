from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Carousel(models.Model):
    background = models.ImageField(upload_to='sliders/')
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title

class Category(models.Model):
    category = models.CharField(max_length=255)
    background = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.category
     
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    price = models.FloatField()
    photo = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.description

class ProductSold(models.Model):
    dealer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_made', default=None)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_received', default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    total = models.FloatField(default=None)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} {self.dealer}"



