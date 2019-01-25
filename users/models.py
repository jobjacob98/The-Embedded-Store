from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField("Address", max_length=1024)
    pin_code = models.CharField("Pin Code", max_length=12)
    city = models.CharField("City", max_length=512)
    country = models.CharField("Country", max_length=512)
    def __str__(self):
        return f'{self.user.username} Account'

class Cart(models.Model):
    cart_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=50, null=True)
    product_price = models.IntegerField(null=True)
