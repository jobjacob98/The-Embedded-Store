from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(max_length=50)
    def __str__(self):
        return self.cat_name

class Product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.IntegerField()
    product_img = models.ImageField(upload_to='product_imgs', null=True)
    def __str__(self):
        return self.product_name
