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


def product_list(request):
	product = Product.objects.all();
	context = {'product':product}
	return render(request,'product.html',context);
	
def edit_product(request, pid):
	print "entered this function"
	product = Product.objects.get(product_id=pid)
	context = {'product':product}	
	return render(request,'edit_product.html',context)

@csrf_exempt	
def update_product(request):
	d =  json.loads(request.body)	  
	product_id = d['product_id']
	name = d['name']
	manufacturer = d['manufacturer']
	category = d['category']
	min_restock = d['min_restock']
	status = d['status']
	product = Product.objects.get(product_id = product_id)
	product.name = name
	product.manufacturer = manufacturer
	product.category = category
	product.min_restock = min_restock
	product.status = status
	product.save()
	payload = {	
	 'messageupdate' : 1,
	}
	data = json.dumps(payload)
	print data;
	return HttpResponse(data,mimetype='application/json')	
	

		
	  
	  