from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/', views.loginVendor, name='loginVendor'),
    path('register/', views.createVendor, name='registerVendor'),
    path('logout/', views.logoutVendor, name='logoutVendor'),

    path('newview/', views.newview),

    path('profile/', views.vendorProfile, name='vendorprofile'),
    path('editprofile/', views.editprofileVendor, name='editprofilevendor'),


    # shop urls ---->
    path('shopview/<str:pk>/', views.shopview, name='shopview'),
    path('editshop/<str:pk>/', views.editShop, name='editshop'),
    path('createshop/', views.createShop, name='createshop'),
    path('deleteshop/<str:pk>/', views.deleteShop, name='deleteshop'),

    # product urls ---->
    path('createproduct/<str:pk>', views.createProduct, name='createproduct'),
    path('editproduct/<str:pk>', views.editProduct, name='editproduct'),
    path('deleteproduct/<str:pk>', views.deleteProduct, name='deleteproduct'),


    path('productdetails/<str:pk>', views.productdetails, name='productdetails'),
    path('cart/<str:pk>/', views.cart, name='cart'),
    path('clearcart/<str:pk>/', views.clearcart, name='clearcart'),

    path('checkout/<str:pk>/', views.checkout, name='checkout'),
    path('checkoutconfirmation/<str:pk>/', views.checkout_confirmation, name='checkout_confirmation'),
    path('confirmation/<str:pk>', views.confirmation, name='confirmation'),
    path('purchasehistory/<str:pk>/', views.purchasehistory, name='purchasehistory'),
    path('orderhistory/<str:pk>/',views.orderhistory, name='orderhistory'),
    # path('purchasehistory/<str:pk>/', views.purchasehistory, name='purchasehistory'),
    # # path('accounts/password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # # path('profile/', views.customer_profile, name='customerprofile'),
    # # path('editprofile/', views.edit_profile, name='editprofile'),
    # # path(),


]