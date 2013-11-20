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


def restock_qty(request):
	print "entered restock method"
	inventory = Inventory.objects.all()
	requests = RequestDetails.objects.all()
	
	for i in inventory:
		batches = Inventory.objects.filter(product_id_id=i.product_id_id)
		tot = 0 
		for b in batches:
			tot += b.qty
		product = Product.objects.get(product_id = i.product_id_id)	
		if tot<=product.min_restock:		
			pr_requests = RequestDetails.objects.filter(product_id=i.product_id_id)
			if not pr_requests:
				if not requests:
					id = 1
				else:
					r = RequestDetails.objects.all().order_by('-request_id')
					id = r[0].request_id + 1
				qtyVal = 100*(product.min_restock-i.qty)
				newRequest = RequestDetails(request_id = id, product_id = i.product_id_id, qty = qtyVal, status='ADDED', request_date = date.today())
				newRequest.save()						
				print newRequest.qty
	return HttpResponse('yo')		
			