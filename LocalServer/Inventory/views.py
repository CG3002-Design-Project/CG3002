# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory
from Transaction.models import Transaction
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os

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
	inventory = Inventory.objects.get(product_id = d['barcode'])
	payload = {}
	if (inventory.cost_price is not None):
		 payload = {
			'price' : str(inventory.cost_price),
			'barcode' : str(inventory.product_id),
			'name' : str(inventory.name),
			'qty' : str(d['qty'])
		 }
	else:
		payload = {
			'price' : -1
		 }
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
	
	
	