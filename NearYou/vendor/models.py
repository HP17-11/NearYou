import uuid
from django.db import models
from django.contrib.auth.models import User
# from LocalMarket.models import Product
from django.core.validators import RegexValidator

# Create your models here.
class vendor(User):
    vendor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone_regex = (RegexValidator
                   (regex=r'^\d{10}$',
                    message="The phone number should be of 10 digits long"))

    phone_number = models.CharField(validators=[phone_regex], max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class shop(models.Model):
    shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gst_no = models.CharField(max_length=200, default=None)
    shop_name = models.CharField(max_length=200)
    shop_image = models.ImageField(
        null=True, blank=True, upload_to='shoppics/', default="shoppics/groceryShop.jpeg")
    vendor_id = models.ForeignKey(vendor, on_delete=models.CASCADE)
    shop_address = models.CharField(max_length=200, default=None)
    shop_city = models.CharField(max_length=100, default=None)
    shop_zip_code = models.CharField(max_length=20, default=None)

    def __str__(self):
        return f"{self.shop_name}"