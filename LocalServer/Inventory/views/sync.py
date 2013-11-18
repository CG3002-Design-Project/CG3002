from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory, RequestDetails
from Inventory.models import Product
from Inventory.models import Transaction
import datetime
from decimal import *
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
import time
import serial
from restock import *

shopid = 00000005
cashid = 00001

hq_host_inventory = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processInventory"
hq_host_transaction = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processTransactions"
hq_host_request = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processRequest"
hq_host_product = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processProduct"
hq_host_product_pull = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/receiveProduct"
hq_host_inventory_pull = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/receiveInventory"

def sync_function(request):
	return render(request,'sync.html');

	
def request_details_sync(request):
	print "entered this method"
	restock_qty(request);
	print "entered request details sync with hq"
	request = RequestDetails.objects.all()
				
	if(request is not None):
		list = []
		for i in request:
			list.append({'qty' : str(i.qty), 
						'request_id' : str(i.request_id),
						'product_id': str(i.product_id),
						'request_date': str(i.request_date),
						 'shopid': str(shopid)}) 
		payload = {
				'request_details': list	
		}
		data = json.dumps(payload)
		headers = {'content-type': 'application/json'}
		res = requests.post(hq_host_request ,data,headers = headers)
	return render(request,'sync_function.html');
	
def inventory_sync(request):
	print "entered sync with hq"
	inventory = Inventory.objects.all()
				
	if(inventory is not None):
		list = []
		for i in inventory:
			list.append({'qty' : str(i.qty), 
						'batchid' : str(i.batch_id),
						'product_id': str(i.product_id_id),
						 'minimum_qty': str(i.minimum_qty),
						 'selling_price' : str(i.selling_price),
						 'shopid': shopid}) 
		payload = {
				'inventory': list	
		}
		data = json.dumps(payload)
		print data;
		headers = {'content-type': 'application/json'}
		res = requests.post(hq_host_inventory ,data,headers = headers)
	return render(request,'sync_function.html');
	
	
	
def product_sync(request):
	print "entered sync with hq"
	product = Product.objects.all()
				
	if(product is not None):
		list = []
		for i in product:
			list.append({'product_id': str(i.product_id),
						'name': i.name, 
						'manufacturer': i.manufacturer,
						'category': i.category,
						 'min_restock': i.min_restock,
						 'shopid': shopid}) 
		payload = {
				'product': list	
		}
		data = json.dumps(payload)
		headers = {'content-type': 'application/json'}
		res = requests.post(hq_host_product ,data,headers = headers)
	return render(request,'sync_function.html');	
	

def pull_inventory_from_hq(request):
	print "entered pull from hq"
	payload = {'shopid': shopid }
	r = requests.get(hq_host_inventory_pull,params=payload)
	data = json.loads(r.text)
	invent = data['inventory']
	for i in invent:
		product_id = int(i['productid'])
		batch_id = int(i['batchid'])
		qty = int(i['qty'])
		cost_price = Decimal(i['cost_price'])
		expiry_date = i['expiry_date']
		selling_price = Decimal(i['selling_price'])
		minimum_qty = int(i['minimum_qty'])
		
		inventor = Inventory.objects.filter(product_id=product_id, batch_id=batch_id) 

		for inventory in inventor:
			if(inventory is not None): 
				inventory.product_id = product_id
				inventory.batch_id = batch_id
				inventory.qty = qty
				inventory.cost_price = cost_price
				if(expiry_date != 'None'):
					expiry_date = datetime.datetime.strptime(i['expiry_date'], '%Y-%m-%d').date()
					inventory.expiry_date = expiry_date
				inventory.selling_price = selling_price
				inventory.minimum_qty = minimum_qty
				inventory.save();
			else:
				if(expiry_date != 'None'):
					expiry_date = datetime.datetime.strptime(i['expiry_date'], '%Y-%m-%d').date()
					inventory.expiry_date = expiry_date
				inventory_new = Inventory(product_id_id = product_id,
									  batch_id = batch_id,
									  qty = qty,
									  cost_price = cost_price,
									  expiry_date = expiry_date,
									  selling_price = selling_price,
									  minimum_qty = minimum_qty);
			
				inventory_new.save()
	return render(request,'sync_function.html');	

def pull_product_from_hq(request):
	print "entered product pull from hq"
	payload = {'shopid': shopid }
	r = requests.get(hq_host_product_pull,params=payload)
	data = json.loads(r.text)
	product = data['product']
	for i in product:
		product_id = int(i['product_id'])
		name = i['name']
		min_restock = int(i['min_restock'])
		manufacturer = i['manufacturer']
		category = i['category']
		status = i['status']
		product = Product.objects.filter(product_id=product_id);
		
		for p in product:
			if(p is not None):
				p.name = name
				p.min_restock = min_restock
				p.manufacturer = manufacturer
				p.category = category
				p.status = status
				p.save();
			else:
				product_new = Products(product_id = product_id,name=name,min_restock=min_restock,manufacturer=manufacturer,category=category,status=status);
				product_new.save();
	return render(request,'sync_function.html');		
	
def transaction_sync(request):
	print "hello"
	transaction = Transaction.objects.all()
	
	if(transaction is not None):
		list = []
		for i in transaction:
			 list.append({'transaction_id': str(i.transaction_id),
						'transaction_date': str(i.transaction_date),
						 'cashregid' : str(cashid), 
						 'barcode':str(i.product_id),
						 'batchid':str(i.batch_id),
						 'qty': str(i.quantity_sold), 
						 'shopid': str(shopid),
						 'selling_price': str(i.selling_price),
						 'cost_price': str(i.cost_price)})
		payload = {	
				'transaction':list
		}
		data = json.dumps(payload)
		headers = {'content-type': 'application/json'}
		res = requests.post(hq_host_transaction,data,headers = headers)
		return render(request,'sync_function.html');