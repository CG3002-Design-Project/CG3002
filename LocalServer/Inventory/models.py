from django.db import models

# Create your models here.
class Inventory(models.Model):
	#pricing strategy to be added
	minimum_qty = models.DecimalField(max_digits=5,decimal_places=0)
	name = models.CharField(max_length=256)
	selling_price = models.DecimalField(max_digits=6,decimal_places=2)
	qty = models.DecimalField(max_digits=6,decimal_places=0)
	manufacturer = models.CharField(max_length=256)
	batch_id = models.DecimalField(max_digits=5,min_digits=5,decimal_places=0)
	cost_price = models.DecimalField(max_digits=6,decimal_places=2)
	product_id = models.DecimalField(max_digits=8,min_digits = 8, decimal_places=0)
	category = models.CharField(max_length=256)
	expiry_date = models.DateField(auto_now=False,auto_now_add=False)
	