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


def update_perishable_price(request):
	print "entered this method";
	inventory = Inventory.objects.all();
	for i in inventory:
		if(i.expiry_date is not None):
			if(i.qty <= i.minimum_qty):
				i.selling_price = i.selling_price - (i.selling_price * (i.strategy_percentage*Decimal(0.01)))
				i.save()
	return HttpResponse("pricing persishables");	

def update_nonperishable_price(request):		
	print "entered this method for non perishables";
	inventory = Inventory.objects.all();
	for i in inventory:
		if(i.expiry_date is None):
			if(i.qty <= i.minimum_qty):
				i.selling_price = i.selling_price + (i.selling_price * (i.strategy_percentage*Decimal(0.001)))
				i.save()
	return HttpResponse("pricing non-persishables");			
				