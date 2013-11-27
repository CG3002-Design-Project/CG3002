from django.core.management.base import BaseCommand, CommandError
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


class Command(BaseCommand):
    help = 'delete batch'

    def handle(self, **options):
       
		inventory = Inventory.objects.all()
		requests = RequestDetails.objects.all()
		
		for i in inventory:
			batches = Inventory.objects.filter(product_id_id=i.product_id_id)
			tot = 0 
			for b in batches:
				tot += b.qty
			product = Product.objects.get(product_id = i.product_id_id)	
			if tot > product.min_restock:	
				pr_requests = RequestDetails.objects.filter(product_id=i.product_id_id)
				if pr_requests not None:
					pr_requests.delete()
            
# To set this up:
# 1. Create file pricing_strategy_cronjob
# 2. In the file, add below line 
# 0 0 * * 0-6 python manage.py recalculate_price 
# (min hr day month day_run Command) << File format, this job runs recalculate_price.py every day at 12am
# 3. On Unix system, run this to set it up: crontab -a pricing_strategy_cronjob                 