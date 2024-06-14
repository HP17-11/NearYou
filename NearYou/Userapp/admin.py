from django.contrib import admin
from django.db import models
from .models import Product, Customer, OrderItem, Payment, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Order)