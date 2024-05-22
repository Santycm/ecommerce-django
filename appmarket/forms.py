from django import forms
from .models import Category, Product

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class SignUpForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    lname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telephone'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    cpassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm your password'}))

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
    

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'stock', 'price', 'photo']


   