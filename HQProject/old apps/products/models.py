from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=256)
    manufacturer = models.CharField(max_length=256)
   
class Store(models.Model):
    region = models.CharField(max_length=256)
    address = models.CharField(max_length=256) 
