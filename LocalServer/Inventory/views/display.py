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


def createConnection():
	if os.name == 'posix':
		PORT = "/dev/ttyUSB0"
	elif os.name == "nt":
		PORT = "COM1"
	return serial.Serial(PORT,9600,timeout = 0.5)	

def write_to_display(name,price):
	ser = createConnection()
	print ser.name;
	ser.write(name);
	name_ack = ser.read(8);
	ser.write(price);
	price_ack = ser.read(8);

@csrf_exempt	
def setDisplayID(request):
	print "reached setDisplayID method"
 	d =  json.loads(request.body)
	print d['barcode']
	print d['batchid']
	print d['display_id']
	inventory = Inventory.objects.get(product_id_id = d['barcode'], batch_id=d['batchid'])
	product = Product.objects.get(product_id = d['barcode']);
	payload = {
		'price' : str(inventory.selling_price),
		'name': str(product.name),
		'error' : 1
	}

	inventory.display_id = Decimal(d['display_id']);
	inventory.save();
	payload = {
			'error' : 1
		 }	
	data = json.dumps(payload);
	return HttpResponse(data,mimetype='application/json')

@csrf_exempt
def display(request):
	print "reached display method"
	d =  json.loads(request.body)
	print d['barcode']
	print d['batchid']
	print d['display_id']
	payload = {}
	
	inventory = Inventory.objects.filter(product_id_id = d['barcode'], batch_id=d['batchid'])
	if not inventory:
		#product doesn't exist
		payload = {
			'error': -1
		}	
	elif (inventory[0].display_id):
		product = Product.objects.get(product_id = d['barcode']);
		payload = {
			'error': -2,
		}
	else:
		 payload = {
			'error' : 1
		 }		 
	data = json.dumps(payload)
	print data;
	return HttpResponse(data,mimetype='application/json')	