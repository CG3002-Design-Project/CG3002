from django.db import models

# Create your models here.

class Store(models.Model):	
    store_id = models.DecimalField(max_digits=8,decimal_places=0,primary_key=True)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256,null=True)
    country = models.CharField(max_length=256)
    region = models.CharField(max_length=256)
    address = models.CharField(max_length=256) 
