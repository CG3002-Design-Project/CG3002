from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Inventory(models.Model):
	#pricing strategy to be added
	product_id = models.ForeignKey('Product')
	qty = models.PositiveIntegerField(validators=[MaxValueValidator(531441), MinValueValidator(0)])
	selling_price = models.DecimalField(max_digits=6,decimal_places=2) #create validator
	minimum_qty = models.PositiveIntegerField(validators=[MaxValueValidator(531441), MinValueValidator(0)])
	batch_id = models.PositiveIntegerField(validators=[MaxValueValidator(59049)])
	cost_price = models.DecimalField(max_digits=6,decimal_places=2)
	expiry_date = models.DateField(auto_now=False,auto_now_add=False, null=True)
	min_restock = models.PositiveIntegerField(validators=[MaxValueValidator(531441)])
	strategy_percentage = models.DecimalField(max_digits=6,decimal_places=2)
	display_id = models.DecimalField(max_digits=6,decimal_places=2, null = True)
	
class Product(models.Model):
	product_id = models.PositiveIntegerField(validators=[MaxValueValidator(43046721)])
	name = models.CharField(max_length=256)
	manufacturer = models.CharField(max_length=256)
	category = models.CharField(max_length=256)
	status = models.CharField(max_length=256)
	
class RequestDetails(models.Model):
	request_id = models.PositiveIntegerField(validators=[MaxValueValidator(43046721)], primary_key=True)
	product_id = models.PositiveIntegerField(validators=[MaxValueValidator(43046721)])
	qty = models.PositiveIntegerField(validators=[MaxValueValidator(531441)])
	status = models.CharField(max_length=256)
	request_date = models.DateField(auto_now=False,auto_now_add=False)
	
class Transaction(models.Model):
	transaction_id = models.PositiveIntegerField(validators=[MaxValueValidator(43046721)])
	transaction_date = models.DateField(auto_now=False,auto_now_add=False)
	product_id = models.PositiveIntegerField(validators=[MaxValueValidator(43046721)])
	quantity_sold = models.PositiveIntegerField(validators=[MaxValueValidator(531441)])
	batch_id = models.PositiveIntegerField(validators=[MaxValueValidator(59049)])
	cachier_id = models.PositiveIntegerField(validators=[MaxValueValidator(59049)])