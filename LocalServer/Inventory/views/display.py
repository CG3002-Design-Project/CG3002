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
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 

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
        PORT = "COM20"
    return serial.Serial(PORT, 9600, timeout = 0.0)



@csrf_exempt
def create_lcd_list(request):   
    inventory = Inventory.objects.all()
    list = []
    for i in inventory:
        if i.display_flag == 'True':
            if i.display_id is not None:
                list.append(str(i.display_id))
    payload = {'lcdlist':list}			
    data = json.dumps(payload)
    return HttpResponse(data,mimetype='application/json')	
	
	
@csrf_exempt
def write_to_display(request):
	d =  request.GET['id']
	inventory = Inventory.objects.get(display_id = int(d))
	inventory.display_flag = 'False'
	inventory.save()
	product = Product.objects.get(product_id=inventory.product_id_id)
	s = str(product.name)
	sp = str(inventory.selling_price)
	payload = {}
	payload = {'name':s,'sp':sp}
	data = json.dumps(payload)
	print data;
	return HttpResponse(data,mimetype='application/json')
	
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
	inventory.display_flag = 'True' 
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