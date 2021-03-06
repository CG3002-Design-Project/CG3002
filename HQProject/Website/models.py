from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class StorePivot(models.Model):
        store_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)],primary_key=True)
        region = models.CharField(max_length=256)
        avg_revenue = models.DecimalField(max_digits=6,decimal_places=2)

class Employee(models.Model):
        user = models.OneToOneField(User)
        employee_email = models.CharField(max_length=256)
        store_id = models.ForeignKey('Store')
        designation = models.CharField(max_length=256)
        salary = models.DecimalField(max_digits=6,decimal_places=2)
        annual_bonus = models.DecimalField(max_digits=6,decimal_places=2)
        address = models.CharField(max_length=5000)
        phone = models.DecimalField(max_digits=15,decimal_places=0)

class Inventory(models.Model):
        #pricing strategy to be added
        product_id = models.ForeignKey('Product')
        store_id = models.ForeignKey('Store')
        qty = models.PositiveIntegerField(validators=[MaxValueValidator(99999), MinValueValidator(0)])
        selling_price = models.DecimalField(max_digits=6,decimal_places=2) #create validator
        minimum_qty = models.PositiveIntegerField(validators=[MaxValueValidator(99999), MinValueValidator(0)])
        batch_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
        cost_price = models.DecimalField(max_digits=6,decimal_places=2)
        expiry_date = models.DateField(auto_now=False,auto_now_add=False, null=True, blank=True)
		
class Product(models.Model):
        product_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)],primary_key=True)
        name = models.CharField(max_length=256)
        manufacturer = models.CharField(max_length=256)
        category = models.CharField(max_length=256)
        status = models.CharField(max_length=256)
        min_restock = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
		
		
class Store(models.Model):
        store_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)],primary_key=True)
        address = models.CharField(max_length=256)
        city = models.CharField(max_length=256)
        state = models.CharField(max_length=256)
        country = models.CharField(max_length=256)
        region = models.CharField(max_length=256)	
        lat = models.FloatField("Latitude", blank=True, null=True,help_text="degrees, floating point, South is negative")
        long = models.FloatField("Longtitude", blank=True, null=True,help_text="degrees, floating point, West is negative")
		
		
        
class RequestDetails(models.Model):
        store_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
        request_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)], primary_key=True)
        product_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
        qty = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
        status = models.CharField(max_length=256)
        request_date = models.DateField(auto_now=False,auto_now_add=False)
        
class Transaction(models.Model):
        transaction_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
        transaction_date = models.DateField(auto_now=False,auto_now_add=False)
        product_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
        quantity_sold = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
        batch_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
        cashier_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
        selling_price = models.DecimalField(max_digits=6,decimal_places=2)
        cost_price = models.DecimalField(max_digits=6,decimal_places=2)
        store_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])		
