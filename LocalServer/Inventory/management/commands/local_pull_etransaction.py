from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory
from Inventory.models import Product
from Inventory.models import Transaction, eTransaction
import datetime
from decimal import *
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
import time
import serial
#from restock import *

shopid = 00000001
cashid = 00001

hq_host_inventory = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processInventory"
hq_host_transaction = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processTransactions"
hq_host_request = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processRequest"
hq_host_product = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processProduct"
hq_host_product_pull = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/receiveProduct"
hq_host_inventory_pull = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/receiveInventory"
hq_host_e_pull = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/localPullETransaction"

class Command(BaseCommand):
	help = 'Local pull of eTrans'
	def handle(self, **options):
		print "entered pull from hq"
	
		payload = {'shopid': shopid }
		r = requests.get(hq_host_e_pull,params=payload)
		data = json.loads(r.text)
		etran = data['etran']
		for t in etran:
			transaction_id = int(t['transaction_id'])
			transaction_date = t['transaction_date']
			product_id = int(t['product_id'])
			batch_id = int(t['batch_id'])
			qty = int(t['quantity_sold'])
			cost_price = Decimal(t['cost_price'])
			selling_price = Decimal(t['selling_price'])
			status = t['status']		
			et = eTransaction(transaction_id=transaction_id,transaction_date=transaction_date,product_id=product_id,batch_id=batch_id,quantity_sold = qty,selling_price=selling_price,cost_price=cost_price,status=status) 
			et.save()
			inv = Inventory.objects.get(product_id_id=product_id,batch_id=batch_id)
			inv.qty = inv.qty - qty
			inv.save()		
	