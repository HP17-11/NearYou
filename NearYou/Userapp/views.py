from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib import messages
from vendor.models import shop, vendor
from .forms import CustomerUserForm, ProfileForm, Cart_shopview, OrderIForm
from django.contrib.auth import views as auth_views
# Create your views here.
# from vendor.forms import OrderIForm
from django.contrib.auth.decorators import login_required
from .utils import searchshops
from .models import Customer, Product, Order


# class PasswordResetView(auth_views.PasswordResetView):
user_role = ""
def loginUser(request):

    page = 'login'
    user_auth = None
    #
    # if request.user.is_authenticated:
    #     return redirect('homepage')
    print("hello")
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        print(username)
        # # username = username.lower()
        # password = request.POST.get('password')

        print(password)

        try:
            user = Customer.objects.get(username=username)
            print(user)
            print('hello')
            user_auth = authenticate(request, username=username, password=password)
        except:
            print('User not found')

        if user_auth is not None:
            login(request, user_auth)
            return redirect('customerprofile')

        else:
            print('User does not exists')
            messages.error(request, "Username or Password is invalid!")


    return render(request,'LocalMarket/login-signup.html', {'page':page})

def createUser(request):
    page = 'register'
    form = CustomerUserForm()
    print(request)
    if request.method == 'POST':
        form = CustomerUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User is created successfully")
            # login(request, user)
            print(user)
            return redirect("loginUser")
        else:
            print(request,'an error has occured while login')

    return render(request, 'LocalMarket/login-signup.html', {'page':page, 'form':form})

def logoutUser(request):
    logout(request)
    return redirect('loginUser')
def homepage(request):
    page = 'homepage'
    user_role = None
    order_current = None

    if request.user.is_authenticated:
        try:
            user_consumer = Customer.objects.get(username=request.user.username)
            user_role = 'customer'
            check_order_id = request.session.get('order.id', None)
            print(check_order_id)
            if check_order_id is None:
                print("You don't have any ongoing orders")
            else:
                order_current = check_order_id
        except:
            user_consumer = vendor.objects.get(username=request.user.username)
            user_role = 'vendor'
        print(user_consumer)

    # return render(request, 'navbar.html', {})
    print(user_role)
    print(request.user.username)

    shops_all = shop.objects.all()
    shops, search_query = searchshops(request)
    print(shops)

    # return HttpResponse('<h1>This is homepage</h1>')
    return render(request, '../templates/homepage.html', {'page':page, 'shops_all': shops_all, 'user_role': user_role, 'search_query': search_query, 'shops': shops, 'order_current': order_current})

def empty_cart(request):
    if request.user.is_authenticated:
        messages.error(request, "You don't have any ongoing Order")
        return redirect('homepage')
    else:
        messages.error(request, "Login First")
        return redirect('loginUser')

@login_required(login_url='loginUser')
def customer_profile(request):

    user_role='customer'

    user = request.user
    print(user)
    customer = Customer.objects.get(username=user)
    print(customer)
    return render(request, 'LocalMarket/customer_profile.html', {'customer':customer, 'user_role': user_role})

@login_required(login_url='loginUser')
def edit_profile(request):

    user_role = 'customer'

    user = request.user
    customer = Customer.objects.get(username=user.username)
    form = ProfileForm(instance=customer)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=customer)
        print(form.is_valid())
        if form.is_valid():

            form.save()

            return redirect('customerprofile')

    context = {'form': form, 'customer': customer, 'user_role': user_role}
    return render(request, 'LocalMarket/profile_form.html', context)

def aboutuspage(request):
    user_role = None
    if request.user.is_authenticated:
        try:
            user_consumer = Customer.objects.get(username=request.user.username)
            user_role = 'customer'
        except:
            user_consumer = vendor.objects.get(username=request.user.username)
            user_role = 'vendor'
        print(user_consumer)
    return render(request, 'LocalMarket/aboutuspage.html', {'user_role': user_role})

def contactuspage(request):
    user_role = None
    if request.user.is_authenticated:
        try:
            user_consumer = Customer.objects.get(username=request.user.username)
            user_role = 'customer'
        except:
            user_consumer = vendor.objects.get(username=request.user.username)
            user_role = 'vendor'
        print(user_consumer)

    return render(request, 'LocalMarket/contactuspage.html', {'user_role': user_role})

def termspage(request):
    user_role = None
    if request.user.is_authenticated:
        try:
            user_consumer = Customer.objects.get(username=request.user.username)
            user_role = 'customer'
        except:
            user_consumer = vendor.objects.get(username=request.user.username)
            user_role = 'vendor'
        print(user_consumer)
    return render(request, 'LocalMarket/termspage.html', {'user_role': user_role})


@login_required(login_url='loginUser')
def orderdetails(request,pk):
    page = 'Order Details'
    user_role = 'customer'
    order_item = Order.objects.get(order_id=pk)
    orderitems = order_item.orderitem_set.all()
    no_of_items = len(order_item.orderitem_set.all())
    delivery = 5
    orderitemamount = 0
    orderwith_product=[]
    for orderitem in orderitems:
        orderitemamount = orderitemamount + float(orderitem.amount)
    print(orderitemamount)
    gst = round(float(orderitemamount) * 0.13, 2)
    total = gst + delivery + orderitemamount
    return render(request, 'LocalMarket/orderdetails.html',
                  {'orderwith_product':orderwith_product, 'orderitems':orderitems, 'page': page, 'no_of_items': no_of_items, 'order_item': order_item, 'delivery': delivery,
                   'orderitemamount': orderitemamount,'gst': gst, 'total': total, 'user_role': user_role})



