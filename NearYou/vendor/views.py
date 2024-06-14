from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from .forms import VendorUserForm, ShopForm, ProductForm, ProfileVendorForm, Order_ind_form, OrderIForm
from LocalMarket.models import Customer, Order, OrderItem
from django.contrib.auth import views as auth_views
from .models import vendor, shop
from LocalMarket.models import Product
from .utils import searchproducts, finaltotal
from LocalMarket.forms import Cart_shopview

# Create your views here.
from django.contrib.auth.decorators import login_required


# --------------- Vendor Profile VIEWS ----------------------

user_role = None
def loginVendor(request):

    page = 'login'
    user_auth = None
    #
    # if request.user.is_authenticated:
    #     return redirect('homepage')
    print("vendor")
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        print(username)
        # # username = username.lower()
        # password = request.POST.get('password')

        print(password)

        try:
            user = vendor.objects.get(username=username)
            print(user)
            user_auth = authenticate(request, username=username, password=password)
        except:
            print('vendor not found')
            # messages.error(request, "The Vendor not found!")

        if user_auth is not None:
            user_role = 'vendor'
            login(request, user_auth)
            return redirect('vendorprofile')

        else:
            print('Username or Password is incorrect')
            messages.error(request, "Username or Password is invalid!")

    return render(request, 'vendor/login_signup.html', {'page':page})

def createVendor(request):
    page = 'register'
    form = VendorUserForm()
    print(request)
    if request.method == 'POST':
        form = VendorUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Vendor created successfully")
            print(user)
            return redirect("loginVendor")
        else:
            messages.error(request, 'an error has occured while login')

    return render(request, 'vendor/login_signup.html', {'page':page, 'form':form})

def logoutVendor(request):
    logout(request)
    return redirect('loginVendor')

@login_required(login_url='loginVendor')
def editprofileVendor(request):
    page = 'editProfileVendor'
    user_role = 'vendor'
    vendor_n = request.user
    vendor_v = vendor.objects.get(username=vendor_n.username)
    form = ProfileVendorForm(instance=vendor_v)

    if request.method == 'POST':
        form = ProfileVendorForm(request.POST, instance=vendor_v)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('vendorprofile')

    context = {'form': form, 'vendor': vendor_v, 'user_role': user_role, 'page': page}
    return render(request, 'vendor/edit_product_shop_vendor_form.html', context)

def newview(request):
    page = 'newview'
    return render(request, 'vendor/newview.html')


def vendorProfile(request):
    page = 'vendorProfile'
    user_role = 'vendor'
    vendor_user = vendor.objects.get(username=request.user.username)
    shops = vendor_user.shop_set.all()
    return render(request, 'vendor/vendorProfile.html', {'page':page, 'user_role':user_role, 'vendor_user':vendor_user, 'shops':shops})


# --------------- Shop VIEWS ----------------------
@login_required(login_url='loginVendor')
def createShop(request):
    page = 'createShop'
    user_role = 'vendor'

    vendor_shop = vendor.objects.get(username=request.user.username)

    form = ShopForm()
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.vendor_id = vendor_shop
            shop.save()
            messages.success(request, 'Shop was added successfully!')
            return redirect('vendorprofile')

    return render(request, 'vendor/create_shop_product.html', {'page':page, 'form':form, 'user_role': user_role})

@login_required(login_url='loginVendor')
def editShop(request, pk):

    page = 'editShop'
    user_role = 'vendor'
    shop_e = shop.objects.get(shop_id=pk)
    form = ShopForm(instance=shop_e)

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop_e)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop changes saved successfully.')
            return redirect('vendorprofile')


    return render(request, 'vendor/edit_product_shop_vendor_form.html', {'form': form, 'user_role': user_role, 'page': page, 'shop_e': shop_e})


@login_required(login_url='loginVendor')
def deleteShop(request, pk):
    user_role = 'vendor'
    shop_d = shop.objects.get(shop_id=pk)
    if request.method == 'POST':
        shop_d.delete()
        messages.success(request, 'Shop was deleted successfully!')
        return redirect('vendorprofile')

    context = {'object': shop_d, 'user_role': user_role}
    return render(request, 'delete_template.html', context)

@login_required(login_url='loginVendor')
def inventory(request, pk):
    page = 'inventory'
    user_role = 'vendor'

    shop_p = shop.objects.get(shop_id=pk)
    products, search_query = searchproducts(request, pk)
    return render(request, 'vendor/shopview_inventory.html',
                  {'page': page, 'shop': shop_p, 'products': products, 'search_query': search_query,
                   'user_role': user_role})

def shopview(request, pk):
    page = 'shopview'
    user_role = None
    counter = 0

    if request.user.is_authenticated:
        try:
            user_consumer = Customer.objects.get(username=request.user.username)
            user_role = 'customer'
        except:
            user_consumer = vendor.objects.get(username=request.user.username)
            user_role = 'vendor'
        print(user_consumer)

    print(user_role)
    shop_n = shop.objects.get(shop_id=pk)
    products, search_query = searchproducts(request, pk)
    order_order = ''
    check_order_id = request.session.get('order.id', None)
    if check_order_id is None:
        order_time = 'firsttime'
        form = OrderIForm()
        if counter == 0:
            print("hello")
            if request.method == 'POST':
                print("hello1")
                form = OrderIForm(request.POST)
                form.order_status = 'Ongoing'
                if form.is_valid():
                    order = form.save(commit=False)
                    counter = counter + 1
                    order.user_id = user_consumer
                    order.shop_id = shop_n
                    order.save()
                    request.session['order.id'] = str(order.order_id)
                    print(shop.shop_name)
                    print(order)
                    order_order = request.session['order.id']

    else:
        order_time = 'oldtime'

        order = Order.objects.get(order_id=request.session['order.id'])
        order_order = request.session['order.id']
        print(order)
        print(order_time)
        form = OrderIForm(instance=order)
        if request.method == 'POST':
            form = OrderIForm(request.POST, instance=order)
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                request.session['order.id'] = str(order.order_id)


    newcount = None
    if counter > 0:
        newcount = True

    return render(request, 'vendor/shopview_inventory.html', {'page':page, 'shop':shop_n, 'products':products, 'search_query':search_query, 'user_role': user_role, 'form': form, 'counter': counter, 'newcount': newcount, 'order_time': order_time, 'order_order':order_order})



# --------------- Product VIEWS ----------------------
@login_required(login_url='loginVendor')
def createProduct(request, pk):
    page = 'createProduct'
    user_role = 'vendor'

    shop_p = shop.objects.get(shop_id=pk)
    # vendor_p = vendor.objects.get(username=request.user.username)

    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop_id = shop_p
            product.save()

            messages.success(request, ' Product added successfully!')
            return redirect('shopview', pk=shop_p.shop_id)

    return render(request, 'vendor/create_shop_product.html', {'page': page, 'form': form, 'user_role': user_role})

@login_required(login_url='loginVendor')
def editProduct(request, pk):

    page = 'editProduct'
    user_role = 'vendor'
    product = Product.objects.get(product_id=pk)
    print(product.shop_id)
    shop_p = product.shop_id
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            messages.success(request, 'Changes saved successfully.')
            return redirect('shopview', pk=shop_p.shop_id)


    return render(request, 'vendor/edit_product_shop_vendor_form.html', {'form': form, 'user_role': user_role, 'page': page, 'product':product})


@login_required(login_url='loginVendor')
def deleteProduct(request, pk):
    user_role ='vendor'
    page = 'deleteProduct'
    product = Product.objects.get(product_id=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product was deleted successfully!')
        return redirect('vendorprofile')

    context = {'object': product, 'user_role': user_role}
    return render(request, 'delete_template.html', context)


def orderhistory(request, pk):
    page = 'orderhistory'
    user_role = 'vendor'
    order_data , final_amount = finaltotal(request, pk)

    return render(request, 'vendor/orderhistory.html', {'order_data': order_data,'final_total_amount':final_amount, 'user_role': user_role, 'page': page})




#------ CART VIEWS ---->

def create_ordetItem(request, pk):
    page = 'shopview'
    form = Cart_shopview()
    product = Product.objects.get(product_id=pk)

    if request.method == 'POST':
        form = Cart_shopview(request.POST)
        if form.is_valid:
            cart = form.save(commit=False)
            cart.product_id = product.product_id
            cart.save()


def productdetails(request,pk):
    user_role = 'customer'
    product = Product.objects.get(product_id=pk)
    # cus = request.user
    # shop = product.shop_id
    # customer = Customer.objects.get(username=cus.username)
    # order = Order.objects.get(shop_id=shop, user_id=customer, order_status='Ongoing')
    form = OrderIForm()
    print('orderitem kuch nahi')
    # print(request.session['order.id'])
    # print(request.session)
    check_order_id = request.session.get('order.id')
    print(check_order_id)
    if check_order_id is None:
        form = Order_ind_form()
        print('login required')
        if request.method == 'POST':
            form = Order_ind_form(request.POST)
            if form.is_valid():
                messages.error(request, "Login First")
                return redirect('loginUser')

    else:

        print('hello check')
        order = Order.objects.get(order_id=request.session['order.id'])
        try:
            order_item = OrderItem.objects.get(order=order, product_id=pk)
            print('orderitem second time')
            # order_item = OrderItem.objects.get(orderItem_id=request.session['order_item.id'])
            # order_item = OrderItem.objects.get(product_id=pk)
            form = Order_ind_form(instance=order_item)
            if request.method == 'POST':
                form = Order_ind_form(request.POST, instance=order_item)
                if form.is_valid():
                    order_item = form.save(commit=False)
                    if order_item.order_quantity <= product.quantity:

                        product.quantity = product.quantity - order_item.order_quantity
                        order_item.product_id = product
                        order_item.order = order

                        print(order_item.order_quantity)
                        order_item.save()
                        product.save()

                        messages.success(request, "Updated cart successfully")
                    else:
                        messages.error(request, 'Quantity is more than avialable in Inventory')

        except:

            print('orderfirst time////')
            form = Order_ind_form()
            if request.method == 'POST':
                form = Order_ind_form(request.POST)
                if form.is_valid():
                    order_item = form.save(commit=False)
                    if order_item.order_quantity <= product.quantity:
                        product.quantity = product.quantity - order_item.order_quantity
                        order_item.product_id = product
                        order_item.order = order
                        print(order_item.order_quantity)
                        order_item.save()
                        product.save()
                        # request.session['order_item.id'] = str(order_item.orderItem_id)
                        messages.success(request, "Added to cart successfully")
                    else:
                        messages.error(request, 'Quantity is more than available in Inventory')

    return render(request, 'vendor/productdetail.html', {'product':product, 'form':form, 'shop':shop, 'user_role':user_role})



@login_required(login_url='loginUser')
def cart(request,pk):
    page = 'cart'
    user_role = 'customer'
    order_item = Order.objects.get(order_id=pk, order_status = 'Ongoing')
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
    return render(request, 'vendor/cart.html',
                  {'orderwith_product':orderwith_product, 'orderitems':orderitems, 'page': page, 'no_of_items': no_of_items, 'order_item': order_item, 'delivery': delivery,
                   'orderitemamount': orderitemamount,'gst': gst, 'total': total, 'user_role': user_role})


@login_required(login_url='loginUser')
def clearcart(request,pk):
    page = 'clearcart'
    user_role = 'customer'
    order = Order.objects.get(order_id=pk)
    if request.method == 'POST':
        order.id = request.session['order.id']
        print(order.id)
        order.id = None
        request.session['order.id'] = order.id
        for orderitem in order.orderitem_set.all():
            product = Product.objects.get(product_id=orderitem.product_id.product_id)
            product.quantity = product.quantity + orderitem.order_quantity
            product.save()
        order.delete()
        messages.success(request, 'Cart cleared successfully!')
        return redirect('homepage')

    context = {'object': order, 'user_role': user_role}
    return render(request, 'delete_template.html', context)



@login_required(login_url='loginUser')
def checkout(request, pk):
    page = 'Checkout'
    customer_c = Customer.objects.get(username=request.user.username)

    if customer_c.address is None or customer_c.city is None or customer_c.zip_code is None:
        messages.error(request, 'First Provide the complete Address!!!')
        return redirect('customerprofile')
    else:
        order_item = Order.objects.get(order_id=pk, order_status='Ongoing')
        orderitems =  order_item.orderitem_set.all()
        no_of_items = len(order_item.orderitem_set.all())
        delivery = 5
        amount = 0
        for orderitem in orderitems:
            amount =amount+float(orderitem.amount)
        print(amount)
        order_item.total_amount = str(amount)
        # amount = order_item.total_amount
        gst = round(float(amount) * 0.13, 2)
        total = gst + delivery + amount
        user_role = 'customer'
        order_item.save()
        context = {'page': page,'no_of_items': no_of_items, 'order_item': order_item, 'delivery': delivery, 'amount': amount,
                   'gst': gst, 'total': total, 'user_role':user_role, 'customer': customer_c}
    return render(request, 'vendor/checkout.html',
                  context)

@login_required(login_url='loginUser')
def checkout_confirmation(request, pk):
    order = get_object_or_404(Order, order_id=pk)

    if request.method == 'POST':
        order.order_status = 'Placed'
        order.id = request.session['order.id']
        print(order.id)
        order.id = None
        request.session['order.id'] = order.id
        order.save()
        return redirect(reverse('confirmation', args=[order.order_id]))
    else:
        return redirect(reverse('checkout', args=[pk]))

@login_required(login_url='loginUser')
def confirmation(request,pk):
    order = get_object_or_404(Order, order_id=pk)
    page = 'Confirmation'
    # order_item1 = Order.objects.get(order_id=pk,order_status='Placed')
    user_role = "customer"
    return render(request,'vendor/confirmation.html',{'order': order, 'user_role': user_role, 'page': page})


@login_required(login_url='loginUser')
def purchasehistory(request,pk):
    page = 'Purchase History'
    user_role = 'customer'
    order_items = Order.objects.filter(user_id=pk)
    order_items_final = order_items.exclude(order_status='ongoing')
    print(order_items_final)
    orders_with_final_amount = []
    for order in order_items_final:
        orderitems = order.orderitem_set.all()
        amount=0
        for orderitem in orderitems:
            amount =amount+float(orderitem.amount)
        order.total_amount = str(amount)
        tax_amount = round(float(order.total_amount) * 1.13, 2)
        finalamount = 5 + tax_amount
        order.save()
        no_of_items = len(order.orderitem_set.all())
        orders_with_final_amount.append({'order': order, 'finalamount': finalamount,'no_of_items':no_of_items})
    return render(request,'vendor/purchasehistory.html',{'orders_with_final_amount':orders_with_final_amount,'page': page,'user_role': user_role})


def orderhistory(request, pk):
    user_role ='vendor'
    page = 'orderhistory'
    order_data , final_amount, total_final_amount = finaltotal(request, pk)
    total_orders = len(order_data)

    return render(request, 'vendor/orderhistory.html', {'user_role': user_role, 'order_data': order_data,'final_total_amount':final_amount, 'total_orders':total_orders,'total_earnings':total_final_amount})


