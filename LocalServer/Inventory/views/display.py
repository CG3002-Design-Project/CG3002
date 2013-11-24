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


def price_display(request):
	print "view all display"
	inventory = Inventory.objects.all();
	list = []
	for i in inventory:
		if i.display_id is not None:
			list.append(i);
			
	context = {'inventory':list}
	return render(request,'display.html',context);

def edit_display(request,did, pid, bid):
	print "entered this function"
	context = {'did':did, 'pid':pid, 'bid':bid}	
	return render(request,'edit_display.html',context)
	
def createConnection():
	if os.name == 'posix':
		PORT = "/dev/ttyUSB0"
	elif os.name == "nt":
		print "os windows"
		PORT = "COM8"
		ser = serial.Serial();
		print "created"
		ser.port = PORT;
		ser.baudrate = 9600
		ser.timeout = 0.5 
		try:
			ser.open()
		except serial.SerialException: 
			ser.close()
			if(ser.isOpen() == False):
				del ser;
				ser = serial.Serial();
				print "creating again"
				ser.port = PORT;
				ser.baudrate = 9600
				ser.timeout = 0.5
				print "poornima here"
				print "closing and opening again"
				ser.open();
		return ser;
		
def write_to_display(name,price):
	print "inside this method"
	ser = createConnection()
	print ser.name;
	a = 'p';
	ser.write(a);
	print "writing didnt give error";
	ser.close();
	#name_ack = ser.read(8);
	#ser.write(price);
	#price_ack = ser.read(8);

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
	#write_to_display(str(product.name), str(inventory.selling_price));
	
	return HttpResponse(data,mimetype='application/json')

@csrf_exempt
def check_display(request):
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