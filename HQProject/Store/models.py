from django.db import models

# Create your models here.

class Store(models.Model):	
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    region = models.CharField(max_length=256)
    address = models.CharField(max_length=256) 