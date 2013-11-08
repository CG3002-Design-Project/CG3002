from django.db import models


# Create your models here.

class Product(models.Model):	
    product_id = models.DecimalField(max_digits=8,decimal_places=0,primary_key=True)
    name = models.CharField(max_length=256)
    manufacturer = models.CharField(max_length=256,default='')
    category = models.CharField(max_length=256,default='')

class Batch(models.Model):	
    minimum_qty = models.DecimalField(max_digits=5,decimal_places=0,default=0)
    selling_price = models.DecimalField(max_digits=5,decimal_places=0,default=0)
    qty = models.DecimalField(max_digits=5,decimal_places=0,default=0)
    expiry_date = models.DateField(auto_now=False,auto_now_add=False,null=True)
    product_id = models.ForeignKey('Product')
    store_id = models.ForeignKey('Store.Store')
    batch_id = models.DecimalField(max_digits=12,decimal_places=0)
	
	
	

