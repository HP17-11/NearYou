# from django.forms import ModelForm
from django import forms
from .models import Customer, OrderItem, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CustomerUserForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email', 'username': 'Username', 'password1': 'Password', 'password2': 'Retype_Password'}

    def __init__(self, *args, **kwargs):
        super(CustomerUserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'cr-form-control'})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_image', 'address', 'city', 'zip_code']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class Cart_shopview(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order_quantity']

    def __init__(self, *args, **kwargs):
        super(Cart_shopview, self).__init__(*args, **kwargs)


class OrderIForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status', 'shop_id']
        widgets = {
            'order_status': forms.HiddenInput(),
            'shop_id': forms.HiddenInput(), # Add this line to include shop_id as a hidden field
        }