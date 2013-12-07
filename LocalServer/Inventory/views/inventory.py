from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
#from django_tables2   import RequestConfig
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory, RequestDetails, Cashier, Employee
from Inventory.models import Product
from Inventory.models import Transaction
from datetime import date
from decimal import *
from django.views.decorators.csrf import csrf_exempt
import json
import os
import time
import serial
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 



@login_required
def inventory_list(request):
	inventory = Inventory.objects.all();
	context = {'inventory':inventory}
	return render(request,'inventory.html',context);

@login_required
def edit_inventory(request, pid, bid):
	print "entered this function"
	inventory = Inventory.objects.get(product_id=pid,batch_id=bid)
	context = {'inventory':inventory}	
	return render(request,'edit_inventory.html',context)

@csrf_exempt	
def update_inventory(request):
		  
	d =  json.loads(request.body)
	product_id = d['product_id_id']
	batch_id = d['batch_id']
	qty = d['qty']
	selling_price = d['selling_price']
	minimum_qty = d['minimum_qty']
	cost_price = d['cost_price']
	strategy_percentage = d['strategy_percentage']
	display_id = d['display_id']
	
	inventory = Inventory.objects.get(product_id_id = product_id, batch_id = batch_id)
	
			
	inventory.product_id_id = product_id
	inventory.batch_id = batch_id
	inventory.qty = qty
	inventory.selling_price = selling_price
	inventory.minimum_qty = minimum_qty
	inventory.cost_price = cost_price
	inventory.strategy_percentage = strategy_percentage
	inventory.save()
		
	payload = {	
	 'messageupdate' : 1,
	}
	data = json.dumps(payload)
	print data;
	return HttpResponse(data,mimetype='application/json')	
	

		
	  
	  