from collections import defaultdict
from itertools import groupby
from django.http import JsonResponse as json
from django.shortcuts import get_object_or_404, redirect, render

from appmarket.forms import LoginForm, SignUpForm, ProductForm, CarouselForm, CategoryForm
from .models import Carousel, ProductSold, Product, Category
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User


# Create your views here.
def showIndex(request):
    pageTitle = 'Home'
    queryset = Carousel.objects.all()
    return render(request, 'index.html', {'pageTitle': pageTitle, 'carousel':queryset, 'user':userInfo})

def showLogin(request):
    userInfo.clear()
    cartInfo.clear()
    pageTitle = 'Login'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            user = get_object_or_404(User, username=form.user.username)
            userInfo.append({'id':user.id, 'username':user.username, 'name':user.first_name, 'lname':user.last_name, 'is_superuser':user.is_superuser})
            print(userInfo) 
            if user.is_staff and user.is_superuser:
                return redirect('/admin/')
            elif user.is_superuser:
                return redirect('adminsite')
            return redirect('dashboard')
        else:
            txt = "User doesn't exist"
            return render(request, 'login.html', {'error':txt, 'form':LoginForm(), 'pageTitle':pageTitle})
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form':form, 'pageTitle':pageTitle})
    
def showSignUp(request):
    pageTitle = 'SignUp'

    if request.method == 'POST':
        form = SignUpForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return redirect('signup')
    else:
        return render(request, 'signup.html', {'form': SignUpForm(), 'pageTitle':pageTitle}) 


def loadDashboard(request):
    pageTitle = 'Dashboard'
    id = 0
    for item in userInfo:
        id = item['id']
    products = Product.objects.filter(user=id).select_related('category')

    products_category ={}
    for product in products:
        if product.category not in products_category:
            products_category[product.category] = []
        products_category[product.category].append(product)

    return render(request, 'user/dashboard.html', {'pageTitle':pageTitle, 'user':userInfo, 'products':products_category})

def loadAdminSite(request):
    pageTitle = 'Admin Site'
    return render(request, 'admin/admin.html', {'pageTitle':pageTitle, 'user':userInfo, 'users':User.objects.all()})

def deleteUser(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('adminsite')

def loadAdminSiteSliders(request):
    return render(request, 'admin/sliders.html', {'pageTitle':'Sliders', 'user':userInfo, 'carousel':Carousel.objects.all()})


def showAddSlider(request):
    pageTitle = 'Add slider'
    if request.method == 'GET':
        return render(request, 'admin/addslider.html', {'pageTitle':pageTitle, 'form':CarouselForm(), 'user':userInfo})
    else:
        form = CarouselForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sliders')

def showUpdateSlider(request, id):
    pageTitle = 'Update slider'

    slider = get_object_or_404(Carousel, id=id)
    if request.method == 'POST':
        form = CarouselForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            return redirect('sliders')
    else:
        form = CarouselForm(instance=slider)
    return render(request, 'admin/updateslider.html', {'form':form, 'pageTitle':pageTitle, 'user':userInfo}) 

def deleteSlider(request, id):
    slider = get_object_or_404(Carousel, id=id)
    slider.delete()
    return redirect('sliders')

def loadAdminSiteCategories(request):
    categories = Category.objects.all()
    dates_category = []
    for category in categories:
        nproducts = Product.objects.filter(category=category).count()
        dates_category.append({'category':category, 'nproducts':nproducts})
    return render(request, 'admin/categories.html', {'pageTitle':'Categories', 'user':userInfo, 'categories':dates_category})

def showAddCategory(request):
    pageTitle = 'Add category'
    if request.method == 'GET':
        return render(request, 'admin/addcategory.html', {'pageTitle':pageTitle, 'form':CategoryForm(), 'user':userInfo})
    else:
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categories')

def showUpdateCategory(request, id):
    pageTitle = 'Update category'

    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/updatecategory.html', {'form':form, 'pageTitle':pageTitle, 'user':userInfo}) 

def deleteCategory(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('categories')

def showAddProduct(request):
    pageTitle = 'Add product'
    if request.method == 'GET':
        return render(request, 'user/addproduct.html', {'pageTitle':pageTitle, 'form':ProductForm(), 'user':userInfo})
    else:
        name = ''
        for item in userInfo:
            name = item['name']

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_obj = form.save(commit=False)
            product_obj.user = User.objects.get(first_name=name)
            product_obj.save()
            return redirect('dashboard')
    
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
            name = ''
            for item in userInfo:
                name = item['name']
            
            idp = request.POST.getlist('id[]')
            dealer = request.POST.getlist('dealer[]')
            products = request.POST.getlist('product[]')
            counts = request.POST.getlist('count[]')

            for item1, item2, item3, item4 in zip(dealer, products, counts, idp):
                product = Product.objects.get(id=item4)
                actual_stock = product.stock
                price = product.price
                Product.objects.filter(name=item2).update(stock=actual_stock - int(item3))
                ProductSold.objects.create(dealer=User.objects.get(username=item1), customer=User.objects.get(first_name=name), product=Product.objects.get(name=item2), amount=item3, total= int(item3)*price)
                
            cartInfo.clear()
            return redirect('spurchase')
        else:
            return render(request, 'user/cart.html', {'products':cartInfo, 'pageTitle':pageTitle, 'user':userInfo})
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
