from django.urls import path
from . import views



urlpatterns = [
    path('', views.showIndex, name='index'),
    path('login/', views.showLogin, name='login'),
    path('signup/', views.showSignUp, name='signup'),
    path('dashboard/', views.loadDashboard, name='dashboard'),
    path('addproduct/', views.showAddProduct, name='addproduct'),
    path('deleteproduct/<int:id>/', views.deleteProduct, name='deleteproduct'),
    path('updateproduct/<int:id>/', views.updateProduct, name='updateproduct'),
    path('product/<int:id>/', views.viewProduct, name='product'),
    path('addcart/<int:id>/', views.addCart, name='addcart'),
    path('cart/', views.loadCart, name='cart'),
    path('products/', views.showProducts, name='products'),
    path('succesful-purchase/', views.showSPurchase, name='spurchase'),
    path('my-purchases/', views.showPurchases, name='mypurchases'),
    path('clean-cart/', views.cleanCart, name='cleancart'),
]

