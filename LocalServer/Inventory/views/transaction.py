from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory, RequestDetails
from Inventory.models import Product, Cashier, Employee
from Inventory.models import Transaction
from datetime import date
from decimal import *
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
import time
import serial
import datetime
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 

list = []

def cachier_transaction(request):
	print list
	context = {'table':list};
	return render(request,'cachier_transaction.html',context );	

@csrf_exempt	
def add_cachier_transaction(request):
	data = json.loads(request.body)
	batchid = data['batchid']
	productid = data['barcode']
	qty = data['qty']
	price = data['price']
	totol_price = price*qty
	product = Product.objects.get(product_id = data['barcode']);
	name = product.name 
	global list
	list.append({'count':len(list)+1,'batchid':batchid, 'productid':productid, 'qty':qty, 'price':price,'name':name,'totol_price':totol_price })  
	print list
	context = {'table':list};
	return render(request,'cachier_transaction.html',context);	

@login_required
def calculate_transaction(request):
	transaction = Transaction.objects.all();
	context = {'transaction':transaction};
	return render(request,'transaction.html',context);
	
@login_required	
def add_transaction(request):
	return render(request,'add_transaction.html');	

@csrf_exempt	
def check_employee(request):
    id = request.GET['id']
    employee = Employee.objects.filter(employee_id=int(id))
    payload = {}
    if not employee:
        payload = {
            'error': -1
        }		   
    else:
        payload = {
            'error': 1
        }  
    data = json.dumps(payload)
    print data
    return HttpResponse(data,mimetype='application/json')	

	
@csrf_exempt
def checkId(request):   
    print 'hihihi'
    id = request.GET['id']
    cashier = Cashier.objects.filter(cashier_id=int(id))
    payload = {}
    if not cashier:
        payload = {
            'error': -1
        }		   
    else:
	    payload = {
            'error': 0
        }       
    data = json.dumps(payload)
    print data
    return HttpResponse(data,mimetype='application/json')
	
@csrf_exempt
def get_price(request):
    print "reached this method"
    barcode = request.GET['barcode']
    batchid = request.GET['batchid']
    qty = request.GET['qty']
    payload = {}
    print barcode
    print batchid
    print qty
    inventory = Inventory.objects.filter(product_id_id = barcode, batch_id= batchid)
    if not inventory:
        payload = { 'error': -1}	
    elif(inventory[0].qty < int(qty)):
        payload = { 'error': -2, 'qty': inventory[0].qty}
    else:
        payload = { 'error': 1, 'price': str(inventory[0].selling_price)}		
    data = json.dumps(payload)
    print data;
    return HttpResponse(data,mimetype='application/json')

@csrf_exempt
def deduct_inventory(request):
    data = json.loads(request.body)
    inventory = data['product']
    todayDate = datetime.datetime.now()
    b = str(todayDate.year) + '-' + str(todayDate.month) + '-' + str(todayDate.day) 
    trans = Transaction.objects.all().order_by('-transaction_id')
    if not trans:
        id = 1
    else:
        t = Transaction.objects.filter(transaction_date = datetime.datetime.strptime(b, '%Y-%m-%d').date()).order_by('-transaction_id')
        if not t:
            id = 1
        else:
            id = t[0].transaction_id + 1	
    for i in inventory:
        batchid = int(i['batchid'])
        productid=int(i['barcode'])
        qty = int(i['qty'])
        cid = int(i['cid'])
        inv = Inventory.objects.get(product_id_id=productid,batch_id=batchid)
        inv.qty = inv.qty - qty
        inv.save()	
        p = Inventory.objects.get(product_id_id=productid,batch_id=batchid)
        tran = Transaction(transaction_id=id,transaction_date=datetime.datetime.strptime(b, '%Y-%m-%d').date(),product_id=productid,batch_id=batchid,selling_price=p.selling_price,cost_price=p.cost_price,cashier_id=int(cid),quantity_sold=qty)
        tran.save()
    return HttpResponse('hi')
			
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
			'name': str(product.name),
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