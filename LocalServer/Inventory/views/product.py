
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory, RequestDetails
from Inventory.models import Product
from Inventory.models import Transaction
from datetime import date
from decimal import *
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
import time
import serial

def product_list(request):
	product = Product.objects.all();
	context = {'productlist':product}
	return render(request,'product.html',context);
	
def edit_product(request,product_id):
	product = Product.objects.get(product_id=p_id)
	context = {'productlist':product}	
	return render(request,'edit_product.html',context)
	
def update_product(request, p_id):
	if 'product_id' in request.GET and request.GET['product_id'] \
	      and 'name' in request.GET and request.GET['name'] \
		  and 'manufacturer' in request.GET and request.GET['manufacturer'] \
		  and 'category' in request.GET and request.GET['category'] \
		  and 'min_restock' in request.GET and request.GET['min_restock']:
		  
		product_id = requests.GET['product_id']
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
	context = {'product': product}
	return render(request,'product.html',context)
		
	  
	  