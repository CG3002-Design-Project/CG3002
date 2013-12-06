from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from Website.models import Store,Product,Inventory,Transaction

class eTransaction(models.Model):
        transaction_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
        transaction_date = models.DateField(auto_now=False,auto_now_add=False)
        product_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
        quantity_sold = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
        batch_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
        selling_price = models.DecimalField(max_digits=6,decimal_places=2)
        cost_price = models.DecimalField(max_digits=6,decimal_places=2)
        store_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
        status = models.CharField(max_length=256)