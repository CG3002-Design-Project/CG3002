from django.db import models

# Create your models here.
class Inventory(models.Model):
	#pricing strategy to be added
	product_id = models.ForeignKey('Product')
	qty = models.PositiveIntegerField(max_digits=6)
	selling_price = models.DecimalField(max_digits=6,decimal_places=2) #create validator
	minimum_qty = models.PositiveIntegerField(max_digits=6)
	batch_id = models.PositiveIntegerField(max_digits=5,min_digits=5)
	cost_price = models.DecimalField(max_digits=6,decimal_places=2)
	expiry_date = models.DateField(auto_now=False,auto_now_add=False, null=True)
	min_restock = models.PositiveIntegerField(max_digits=6)
	strategy_percentage = models.DecimalField(max_digits=6,decimal_places=2)
    display_id = models.DecimalField(max_digits=6,decimal_places=2, null = True)
class Product(models.Model):
	product_id = models.PositiveIntegerField(max_digits=8, min_digits = 8, primary_key=True)
	name = models.CharField(max_length=256)
	manufacturer = models.CharField(max_length=256)
	category = models.CharField(max_length=256)
	status = models.CharField(max_length=256)
	
class RequestDetails(models.Model):
	request_id = models.PositiveIntegerField(max_digits=8, min_digits = 8, primary_key=True)
	product_id = models.PositiveIntegerField(max_digits=8, min_digits = 8)
	qty = models.PositiveIntegerField(max_digits=6)
	status = models.CharField(max_length=256)
	request_date = models.DateField(auto_now=False,auto_now_add=False)

		
class Transaction(models.Model):
	transaction_id = models.PositiveIntegerField(max_digits=8,min_digits = 8)
	transaction_date = models.DateField(auto_now=False,auto_now_add=False)
	product_id = models.PositiveIntegerField(max_digits=8, min_digits = 8)
	quantity_sold = models.PositiveIntegerField(max_digits=6)
	batch_id = models.PositiveIntegerField(max_digits=5,min_digits=5)
	cachier_id = models.PositiveIntegerField(max_digits=5,min_digits=5)