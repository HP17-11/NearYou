import uuid
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from vendor.models import shop


# Create your models here.
class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop_id = models.ForeignKey(shop, on_delete=models.CASCADE, default=None)
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(null=True, blank=True, upload_to='shoppics/', default="shoppics/vendorShop.jpeg")
    category_choices = [('food_bevarages', 'Food and Bevarages'), ('fruits_veg', 'Fruits and Vegetables'), ('dairy', 'Dairy'), ('other', 'Other') ]
    category = models.CharField(max_length=14,choices=category_choices, default=None)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    price = models.FloatField(validators=[MinValueValidator(0)])
    description = models.TextField()

    def __str__(self):
        return self.product_name + " : " + self.shop_id.shop_name

class Customer(User):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_regex = (RegexValidator
                   (regex=r'^\d{10}$',
                    message="The phone number should be of 10 digits long"))
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='userprofiles/', default="userprofiles/user-default.png")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, null=True, blank=True)
    address = models.CharField(max_length=200, default=None, null=True, blank=True)
    city = models.CharField(max_length=100, default=None, null=True, blank=True)
    zip_code = models.CharField(max_length=20, default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop_id = models.ForeignKey(shop, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_status_choices = [('Ongoing', 'Ongoing'), ('Cancelled', 'Cancelled'), ('Placed', 'Placed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')]
    order_status = models.CharField(max_length=9, choices=order_status_choices, default='Ongoing')
    total_amount = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)

    def __str__(self):
        return self.user_id.first_name + " " + self.total_amount.__str__()



class OrderItem(models.Model):
    orderItem_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    amount = models.FloatField(validators=[MinValueValidator(0)], default=None, null=True, blank=True)

    def __str__(self):
        return f"OrderItem: {self.product_id.product_name} for Order ID: {self.order}"

    def save(self, *args, **kwargs):
        self.amount = self.order_quantity * self.product_id.price
        super().save(*args, **kwargs)


class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_status_choices = [('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')]
    payment_status = models.CharField(max_length=20, choices=payment_status_choices)
    date = models.DateField()
    payment_amount = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment ID: {self.payment_id}"