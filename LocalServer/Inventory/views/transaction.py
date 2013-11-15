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

def calculate_transaction(request):
	return render(request,'calculate_transaction.html');

def price_display(request):
	return render(request,'price_display.html');

@csrf_exempt
def return_price(request):
	print "reached this method"
	d =  json.loads(request.body)
	print d['barcode']
	print d['batchid']
	print d['qty']
	payload = {}
	inventory = Inventory.objects.filter(product_id_id = d['barcode'], batch_id=d['batchid'])
	if not inventory:
		payload = {
			'error': -1
		}	
	elif(inventory[0].qty < int(d['qty'])):
		payload = {
			'error': -2,
			'qty': inventory[0].qty
		}
	else:
		 product = Product.objects.get(product_id = d['barcode']);
		 payload = {
			'price' : str(inventory[0].selling_price),
			'barcode' : str(d['barcode']),
			'batchid': str(d['batchid']),
			'name': str(product.name),
			'qty' : str(d['qty']),
			'error' : 1
		 }
		 inventory[0].qty = inventory[0].qty - int(d['qty']);
		 inventory[0].save();
		 
	data = json.dumps(payload)
	print data;
	return HttpResponse(data,mimetype='application/json')

@csrf_exempt
def save_transaction(request):
	d =  json.loads(request.body)
	t = Transaction.objects.all().order_by('-transaction_id');
	if not t:
		transaction_id = 1;
	else:
		transaction_id = t[0].transaction_id+1;

	for i in d:
		print i;
		t = Transaction(transaction_id= transaction_id, transaction_date = time.strftime("%Y-%m-%d"), product_id = i['barcode'], quantity_sold = i['qty'], batch_id = i['batchid'], cachier_id = "01");
		t.save();
	return HttpResponse("Poornima");


@csrf_exempt
def add_qty_back(request):
	print "reached here";
	d =  json.loads(request.body);
	for i in d:
		print i
		inventory = Inventory.objects.filter(product_id_id = i['barcode'], batch_id=i['batchid'])
		print type(inventory[0].qty);
		inventory[0].qty += int(i['qty']);
		inventory[0].save();
	return HttpResponse("qty added back");