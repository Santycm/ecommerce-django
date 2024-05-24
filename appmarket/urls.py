from django.urls import path
from . import views

urlpatterns = [
    path('', views.showIndex, name='index'),
    path('categories-page/', views.showCategoriesPage, name='categories-page'),
    path('login/', views.showLogin, name='login'),
    path('signup/', views.showSignUp, name='signup'),
    path('adminsite/', views.loadAdminSite, name='adminsite'),
    path('deleteuser/<int:id>', views.deleteUser, name='deleteuser'),
    path('carousels/', views.loadAdminSiteSliders, name='sliders'),
    path('add-slider/', views.showAddSlider, name='addslider'),
    path('update-slider/<int:id>', views.showUpdateSlider, name='updateslider'),
    path('delete-slider/<int:id>', views.deleteSlider, name='deleteslider'),
    path('categories/', views.loadAdminSiteCategories, name='categories'),
    path('add-category/', views.showAddCategory, name='addcategory'),
    path('update-category/<int:id>', views.showUpdateCategory, name='updatecategory'),
    path('delete-category/<int:id>', views.deleteCategory, name='deletecategory'),
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

