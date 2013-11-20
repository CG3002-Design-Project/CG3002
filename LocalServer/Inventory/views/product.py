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

def product_list(request):
	product = Product.objects.all();
	context = {'product':product}
	return render(request,'product.html',context);
	
def edit_product(request, pid):
	print "entered this function"
	product = Product.objects.get(product_id=pid)
	context = {'product':product}	
	return render(request,'edit_product.html',context)
	
def update_product(request):
	if 'product_id' in request.GET and request.GET['product_id'] \
	      and 'name' in request.GET and request.GET['name'] \
		  and 'manufacturer' in request.GET and request.GET['manufacturer'] \
		  and 'category' in request.GET and request.GET['category'] \
		  and 'min_restock' in request.GET and request.GET['min_restock']:
		  
		product_id = request.GET['product_id']
		name = request.GET['name']
		manufacturer = request.GET['manufacturer']
		category = request.GET['category']
		min_restock = request.GET['min_restock']
		product = Product.objects.get(product_id = product_id)
		product.name = name
		product.manufacturer = manufacturer
		product.category = category
		product.min_restock = min_restock
		product.save()
	messageupdate = 'Product has been successfully updated'
	product = Product.objects.all();
	context = {'product':product}
	return render(request,'product.html',context)	
	

		
	  
	  