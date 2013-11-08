from django.db import models

# Create your models here.
class Display(models.Model):
	barcode = models.DecimalField(max_digits=8,decimal_places=0)
	display_id = models.DecimalField(max_digits=8,decimal_places=0)