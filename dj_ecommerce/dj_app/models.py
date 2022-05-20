from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True, unique=True)
    datetime = models.DateTimeField(auto_now=True)
    order_quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
