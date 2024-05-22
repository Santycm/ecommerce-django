from collections import defaultdict
from itertools import groupby
from django.http import JsonResponse as json
from django.shortcuts import get_object_or_404, redirect, render

from appmarket.forms import LoginForm, SignUpForm, ProductForm, UpdateProductForm
from .models import Carousel, ProductSold, Users, Product, Category

# Create your views here.
def showIndex(request):
    pageTitle = 'Home'
    queryset = Carousel.objects.all()
    return render(request, 'index.html', {'pageTitle': pageTitle, 'carousel':queryset, 'user':userInfo})

def showLogin(request):
    userInfo.clear()
    cartInfo.clear()
    pageTitle = 'Login'
    if request.method == 'GET':
        return render(request, 'login.html', {'pageTitle':pageTitle, 'form':LoginForm()})
    else:
        Exist = False
        try:
            Users.objects.get(username=request.POST['username'], password = request.POST['password'])
            Exist = True
        except Users.DoesNotExist:
            return redirect('signup')
        
        if Exist:
            queryset = Users.objects.filter(username=request.POST['username'], password = request.POST['password']).values().first()
            userInfo.append(queryset)
            return redirect('dashboard')
        
def showSignUp(request):
    pageTitle = 'SignUp'
    if request.method == 'GET':
        return render(request, 'signup.html', {'pageTitle':pageTitle, 'form':SignUpForm()})
    else:
        if request.POST['password'] != request.POST['cpassword']:
            return redirect('signup')
        else:
            Users.objects.create(name=request.POST['name'], lname=request.POST['lname'], email=request.POST['email'], telephone=request.POST['telephone'], username=request.POST['username'], password=request.POST['cpassword'])
            return redirect('login')

def loadDashboard(request):
    pageTitle = 'Dashboard'
    id = 0
    for item in userInfo:
        id = item["id"]
    products = Product.objects.filter(user=id).select_related('category')

    products_category ={}
    for product in products:
        if product.category not in products_category:
            products_category[product.category] = []
        products_category[product.category].append(product)

    return render(request, 'user/dashboard.html', {'pageTitle':pageTitle, 'user':userInfo, 'products':products_category})

def showAddProduct(request):
    pageTitle = 'Add product'
    if request.method == 'GET':
        return render(request, 'user/addproduct.html', {'pageTitle':pageTitle, 'form':ProductForm()})
    else:
        name = ""
        for item in userInfo:
            name = item["name"]

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_obj = form.save(commit=False)
            product_obj.user = Users.objects.get(name=name)
            product_obj.save()
            return redirect('dashboard')
        else:
            print('jodidos')
    
def deleteProduct(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('dashboard')

def updateProduct(request, id):
    pageTitle = 'Update product'

    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'user/updateproduct.html', {'form':form, 'pageTitle':pageTitle}) 

def viewProduct(request, id):
    product = get_object_or_404(Product, id=id)
    pageTitle = product.name
    return render(request, 'product.html', {'product':product, 'pageTitle':pageTitle, 'user':userInfo})
    
def addCart(request, id):
    product = get_object_or_404(Product, id=id)
    if userInfo:
        cartInfo.append(product)
        return redirect('cart')
    else:
        return redirect('login')
    

def loadCart(request):
    if userInfo:
        pageTitle = 'Cart'
        if request.method == 'POST':
            name = ""
            for item in userInfo:
                name = item["name"]
            
            idp = request.POST.getlist('id[]')
            dealer = request.POST.getlist('dealer[]')
            products = request.POST.getlist('product[]')
            counts = request.POST.getlist('count[]')

            for item1, item2, item3, item4 in zip(dealer, products, counts, idp):
                product = Product.objects.get(id=item4)
                actual_stock = product.stock
                price = product.price
                Product.objects.filter(name=item2).update(stock=actual_stock - int(item3))
                ProductSold.objects.create(dealer=Users.objects.get(name=item1), customer=Users.objects.get(name=name), product=Product.objects.get(name=item2), amount=item3, total= int(item3)*price)
                
            cartInfo.clear()
            return redirect('spurchase')
        else:
            return render(request, 'user/cart.html', {'products':cartInfo, 'pageTitle':pageTitle})
    else:
        return redirect('login')

def cleanCart(request):
    if cartInfo :
        cartInfo.clear()
        return redirect('cart')
    else:
        return redirect('cart')

def error_404(request, exception):
    return render(request, '404.html')

def showProducts(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products, 'user':userInfo, 'pageTitle':'Products'})

def showSPurchase(request):
    return render(request, 'user/spurchase.html', {'pageTitle':'Successful'})

def showPurchases(request):
    pageTitle = 'My Purchases'
    id = 0
    for item in userInfo:
        id = item["id"]
    products = ProductSold.objects.filter(customer=id).order_by('date', 'time')
    group_history = {}

    for date, items in groupby(products, key=lambda x: x.date):
        group_history[date] = list(items)

    return render(request, 'user/mypurchases.html', {'pageTitle':pageTitle, 'user':userInfo, 'historial_dict':group_history})

userInfo = []
cartInfo = []
