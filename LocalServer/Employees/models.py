from django.db import models

# Create your models here.
class Employees(models.Model):
	name = models.CharField(max_length=256)
	designation = models.CharField(max_length=256)
	employee_id = models.DecimalField(max_digits=8,decimal_places=0)
	salary = models.DecimalField(max_digits=8,decimal_places=0)