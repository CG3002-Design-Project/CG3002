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

class Command(BaseCommand):
    help = 'Pricing Strategy Non-Perishables'

    def handle(self, **options):		
		print "entered this method for non perishables";
		inventory = Inventory.objects.all();
		for i in inventory:
			if(i.expiry_date is None):
				if(i.qty <= i.minimum_qty):
					i.selling_price = i.selling_price + (i.selling_price * (i.strategy_percentage*Decimal(0.001)))
					i.display_flag = 'True'
					i.save()
		return HttpResponse("pricing non-persishables");
            
# To set this up:
# 1. Create file pricing_strategy_cronjob
# 2. In the file, add below line 
# 0 0 * * 0-6 python manage.py recalculate_price 
# (min hr day month day_run Command) << File format, this job runs recalculate_price.py every day at 12am
# 3. On Unix system, run this to set it up: crontab -a pricing_strategy_cronjob                 