from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django_tables2   import RequestConfig
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory, RequestDetails
from Inventory.models import Product
from Inventory.models import Transaction
from datetime import date
from decimal import *
from django.views.decorators.csrf import csrf_exempt
import json
import os
import time
import serial
from Inventory.views.tables import ProductTable

def inventory_list(request):
	inventory = Inventory.objects.all();
	context = {'inventory':inventory}
	return render(request,'inventory.html',context);
	
def edit_inventory(request, pid, bid):
	print "entered this function"
	inventory = Inventory.objects.get(product_id=pid,batch_id=bid)
	context = {'inventory':inventory}	
	return render(request,'edit_inventory.html',context)
	
def update_inventory(request):
		  
	print "reached here"  
	product_id = request.GET['product_id_id']
	batch_id = request.GET['batch_id']
	qty = request.GET['qty']
	selling_price = request.GET['selling_price']
	minimum_qty = request.GET['minimum_qty']
	cost_price = request.GET['cost_price']
	expiry_date = request.GET['expiry_date']
	strategy_percentage = request.GET['strategy_percentage']
	display_id = request.GET['display_id']
	
	inventory = Inventory.objects.get(product_id_id = product_id, batch_id = batch_id)
	
	if request.GET['expiry_date']:
		expiry_date = request.GET['expiry_date']
		if expiry_date == 'None':
			expiry_date = None	
	inventory.product_id_id = product_id
	inventory.batch_id = batch_id
	inventory.qty = qty
	inventory.selling_price = selling_price
	inventory.minimum_qty = minimum_qty
	inventory.cost_price = cost_price
	inventory.expiry_date = expiry_date
	print inventory.strategy_percentage
	print strategy_percentage
	inventory.strategy_percentage = strategy_percentage
	inventory.display_id = display_id
	inventory.save()
		
	messageupdate = 'Product has been successfully updated'
	inventory_result = Inventory.objects.all();
	context = {'inventory': inventory_result}
	return render(request,'inventory.html',context)	
	

		
	  
	  