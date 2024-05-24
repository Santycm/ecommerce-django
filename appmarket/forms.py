from django import forms
from .models import Category, Product, Carousel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if not self.user:
                raise forms.ValidationError('Incorrect credentials')
        return self.cleaned_data

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category', 'background']
        widgets = {
            'category':forms.TextInput(attrs={'placeholder':'Title'})
        }  

class CarouselForm(forms.ModelForm):  
    class Meta:
        model = Carousel
        fields = ['title', 'text', 'background']
        widgets = {
            'title':forms.TextInput(attrs={'placeholder':'Title'}),
            'text':forms.Textarea(attrs={'placeholder':'Text'})
        }    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'stock', 'price', 'photo']
        widgets = {
            'name':forms.TextInput(attrs={'placeholder':'Name'}),
            'description':forms.Textarea(attrs={'placeholder':'Description'}),
            'stock':forms.NumberInput(attrs={'placeholder':'Stock'}),
            'price':forms.NumberInput(attrs={'placeholder':'Price'})
        }    



   