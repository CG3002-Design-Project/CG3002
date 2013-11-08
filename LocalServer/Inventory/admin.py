from django.db import models
from django.contrib import admin
from Inventory.models import Inventory
from Inventory.models import Product
from Inventory.models import RequestDetails
from Inventory.models import Transaction


class InventoryAdmin(admin.ModelAdmin):
	list_per_page = 50
	list_display = ('product_id','batch_id','qty','cost_price','minimum_qty','selling_price','min_restock','strategy_percentage','display_id','expiry_date')
	search_fields = ('product_id','batch_id','qty','cost_price','minimum_qty','selling_price','min_restock','strategy_percentage','display_id','expiry_date')

class ProductAdmin(admin.ModelAdmin):
	list_per_page = 50
	list_display = ('product_id','name','manufacturer','category','status')
	search_fields = ('product_id','name','manufacturer','category','status')

class RequestDetailsAdmin(admin.ModelAdmin):
	list_per_page = 50
	list_display = ('request_id','product_id','qty','status','request_date')
	search_fields = ('request_id','product_id','qty','status','request_date')	

class TransactionAdmin(admin.ModelAdmin):
	list_per_page = 50
	list_display = ('transaction_id','transaction_date','product_id','quantity_sold','batch_id','cachier_id')
	search_fields = ('transaction_id','transaction_date','product_id','quantity_sold','batch_id','cachier_id')
	
admin.site.register(Inventory, InventoryAdmin)	
admin.site.register(Product, ProductAdmin)	
admin.site.register(RequestDetails, RequestDetailsAdmin)	
admin.site.register(Transaction, TransactionAdmin)	