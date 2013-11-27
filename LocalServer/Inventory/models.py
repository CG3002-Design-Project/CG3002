from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

#Create your models here.
class Inventory(models.Model):
	#pricing strategy to be added
	product_id = models.ForeignKey('Product')
	qty = models.PositiveIntegerField(validators=[MaxValueValidator(531441), MinValueValidator(0)])
	selling_price = models.DecimalField(max_digits=6,decimal_places=2) #create validator
	minimum_qty = models.PositiveIntegerField(validators=[MaxValueValidator(999999), MinValueValidator(0)])
	batch_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
	cost_price = models.DecimalField(max_digits=6,decimal_places=2)
	expiry_date = models.DateField(auto_now=False,auto_now_add=False, null=True, blank = True)
	strategy_percentage = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
	display_id = models.DecimalField(max_digits=4,decimal_places=0, null = True, blank = True)
	
class Product(models.Model):
	product_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)],primary_key=True )
	name = models.CharField(max_length=256)
	min_restock = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
	manufacturer = models.CharField(max_length=256)
	category = models.CharField(max_length=256)
	status = models.CharField(max_length=256)
	
class RequestDetails(models.Model):
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
	selling_price = models.DecimalField(max_digits=6,decimal_places=2) #create validator
	cost_price = models.DecimalField(max_digits=6,decimal_places=2)