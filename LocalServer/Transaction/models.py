from django.db import models

# Create your models here.
class Transaction(models.Model):
	transaction_id = models.DecimalField(max_digits=6,decimal_places=0)
	transaction_date = models.DateField(auto_now=False,auto_now_add=False)
	quantity_sold = models.DecimalField(max_digits=5,decimal_places=0)
	selling_price = models.DecimalField(max_digits=5,decimal_places=0)
	product_id = models.DecimalField(max_digits=8,decimal_places=0)
	batch_id = models.DecimalField(max_digits=8,decimal_places=0)