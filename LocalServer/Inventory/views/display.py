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
import serial
import os
import time


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
        PORT = "/dev/ttyUSB1"
    elif os.name == "nt":
        PORT = "COM10"
    return serial.Serial(PORT, 9600, timeout = 0.5)

@csrf_exempt
def write_to_display(request):
	print "inside this method"
	print "connection established"
	inventory = Inventory.objects.all();
	for i in inventory:
		product = Product.objects.get(product_id = i.product_id_id);
		ser = createConnection();
		ser.write("@")
		time.sleep(0.5);
		
		print("writing display id")
		number = i.display_id
		if number is not None:
			while number:
				digit = number % 10
				ser.write(number)
				time.sleep(0.5)
				# do whatever with digit
				number /= 10
			
			print("writing hash")
			ser.write("#")
			time.sleep(0.5);
			
			print("writing product name")		
			s = product.name
			for a in s:
				ser.write(a);
				time.sleep(0.5);
			print("writing dollar")
			ser.write("$")
			time.sleep(0.5);
			
			print("writing price")	
			s = str(i.selling_price)
			for a in s:
				ser.write(a);
				time.sleep(0.5);
			
			ser.close();		
			print "finished writing one";	
	
	print "finished writing all"
	return HttpResponse("success");
	
	
	
@csrf_exempt	
def setDisplayID(request):
	print "reached setDisplayID method"
 	d =  json.loads(request.body)
	print d['barcode']
	print d['batchid']
	print d['display_id']
	inventory = Inventory.objects.get(product_id_id = d['barcode'], batch_id=d['batchid'])
	dis_inventory = Inventory.objects.filter(display_id = d['display_id'])
	print ("same copy");
	for invent in dis_inventory:
		if invent is not None:
			invent.display_id = None;
			invent.save();
		
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