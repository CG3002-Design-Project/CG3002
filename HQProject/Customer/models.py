from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from Website.models import Store,Product,Inventory,Transaction
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    facebook_uid = models.PositiveIntegerField(blank=True, null=True)
    facebook_access_token = models.CharField(blank=True, max_length=255)
    facebook_access_token_expires = models.PositiveIntegerField(blank=True, null=True)

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