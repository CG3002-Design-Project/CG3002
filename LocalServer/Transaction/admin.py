from django.db import models
from django.contrib import admin
from Transaction.models import Transaction

class TransactionAdmin(admin.ModelAdmin):
	list_per_page = 50
	list_display =('transaction_id','transaction_date','product_id','batch_id','quantity_sold','selling_price')
	search_fields = ('transaction_id','transaction_date','product_id','batch_id','quantity_sold','selling_price')
	
admin.site.register(Transaction, TransactionAdmin)