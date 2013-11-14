# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory, RequestDetails
from Inventory.models import Product
from Inventory.models import Transaction
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
import time

shopid = 0001
cashid = 0001
hq_host_inventory = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processInventory"
hq_host_transaction = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processTransactions"

def calculate_transaction(request):
	return render(request,'calculate_transaction.html');

def sync_function(request):
	return render(request,'sync_function.html');

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

def transaction_sync(request):
	print "hello"
	transaction = Transaction.objects.all()
	
	if(transaction is not None):
		list = []
		for i in transaction:
			 list.append({'transactionid': str(i.transaction_id),
						 'cashregid' : str(cashid), 
						 'barcode':str(i.product_id),
						 'qty': str(i.quantity_sold), 
						 'sp': str(10), 
						 'purchasedate':str(i.transaction_date), 
						 'shopid': str(shopid)})
		payload = {
				'shopid': shopid,	
				'transaction':list
		}
		data = json.dumps(payload)
		headers = {'content-type': 'application/json'}
		res = requests.post(hq_host_transaction,data,headers = headers)
		return render(request,'sync_function.html');

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
			
def sync_with_hq(request):
	print "entered sync with hq"
	inventory = Inventory.objects.all()
				
	if(inventory is not None):
		list = []
		for i in inventory:
			list.append({'qty' : str(i.qty), 'batchid' : str(i.batch_id), 'product_id': str(i.product_id)}) 
		payload = {
				'shopid': shopid,
				'inventory': list	
		}
		data = json.dumps(payload)
		headers = {'content-type': 'application/json'}
		res = requests.post(hq_host_inventory ,data,headers = headers)
	return render(request,'sync_function.html');
	
def pull_from_hq(request):
	print "entered pull from hq"
	payload = {'shopid': shopid }
	r = requests.get(hq_host,payload)
	inventory = json.loads(r.text)
	for i in inventory:
		productid = i['productid']
		batchid = i['batchid']
		qty = i['qty']
		costprice = i['costprice']
		sellingprice = i['sellingprice']
		minqty = i['minqty']
		inventory = Inventory.objects.get(product_id=productid, batch_id=batchid) 
		
		iventory.qty = qty
		inventory.cost_price = costprice
		inventory.selling_price = sellingprice
		inventory.minimum_qty = minqty
		
		inventory.save()
		return render(request,'sync_function.html');
	
def restock_qty(request):
	inventory = Inventory.objects.all()
	requests = RequestDetails.objects.all()
	
	for i in inventory:
		batches = Inventory.objects.filter(product_id_id=i.product_id_id)
		tot = 0 
		for b in batches:
			tot += b.qty
		if tot<=i.min_restock:		
			pr_requests = RequestDetails.objects.filter(product_id=i.product_id_id)
			if not pr_requests:
				if not requests:
					id = 1
				else:
					r = RequestDetails.objects.all().order_by('-request_id')
					id = r[0].request_id + 1
				qtyVal = 100*(i.min_restock-i.qty)
				newRequest = RequestDetails(request_id=id,product_id=i.product_id_id,qty=qtyVal,status='False',request_date=date.today())
				newRequest.save()						
				print newRequest.qty
	return HttpResponse('yo')		
			
					
	