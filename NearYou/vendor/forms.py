from django.forms import ModelForm
from django import forms
from .models import vendor, shop
from LocalMarket.models import Product, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class VendorUserForm(UserCreationForm):
    class Meta:
        model = vendor
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'password1', 'password2']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email', 'username': 'Username', 'phone_number': 'Phone Number', 'password1': 'Password', 'password2': 'Retype_Password'}

    def __init__(self, *args, **kwargs):
        super(VendorUserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'cr-form-control'})


class ShopForm(ModelForm):
    class Meta:
        model = shop
        fields = ['shop_name', 'gst_no', 'shop_image', 'shop_address', 'shop_city', 'shop_zip_code']
        labels = {'shop_name': 'Shop Name', 'gst_no': 'GST No', 'shop_image': 'Shop Image', 'shop_city': 'City', 'shop_zip_code': 'Zip Code'}

    def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'quantity', 'category', 'product_image']
        labels = {'product_name': 'Product Name',  'price': 'Price', 'description': 'Description', 'quantity': 'Quantity', 'category': 'Category', 'product_image': 'Product Image'}

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ProfileVendorForm(ModelForm):
    class Meta:
        model = vendor
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(ProfileVendorForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class OrderIForm(ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']


class Order_ind_form(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order_quantity']

        def __init__(self, *args, **kwargs):
            super(Order_ind_form, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'quantity', 'type':'text', 'placeholder' : '.' , 'value': '1' , 'minlength':"1", 'maxlength':"20"})
