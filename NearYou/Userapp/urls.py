from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginUser, name='loginUser'),
    path('', views.homepage , name='homepage'),
    path('register/', views.createUser, name ='registerUser'),
    path('logout/', views.logoutUser, name = 'logoutUser'),
    path('profile/', views.customer_profile, name='customerprofile'),
    path('editprofile/', views.edit_profile, name='editprofile'),
    path('aboutuspage/', views.aboutuspage, name='aboutuspage'),
    path('contactuspage/', views.contactuspage, name='contactuspage'),
    path('termspage/', views.termspage, name='termspage'),
    path('orderdetails/<str:pk>/', views.orderdetails, name='orderdetails'),
    path('emptycart/', views.empty_cart, name='emptycart'),


    # path(),


]