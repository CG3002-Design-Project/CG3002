from django.db import models
from django.contrib import admin
from Inventory.models import Inventory

class InventoryAdmin(admin.ModelAdmin):
	list_per_page = 50
	list_display = ('product_id','batch_id','name','category','manufacturer','qty','cost_price','minimum_qty','selling_price')
	search_fields = ('product_id','batch_id','name','category','manufacturer','qty','cost_price','minimum_qty','selling_price')
	
admin.site.register(Inventory, InventoryAdmin)	