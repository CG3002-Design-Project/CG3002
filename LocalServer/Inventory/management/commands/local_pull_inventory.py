from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory
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
#from restock import *

shopid = 00000005
cashid = 00001

hq_host_inventory = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processInventory"
hq_host_transaction = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processTransactions"
hq_host_request = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processRequest"
hq_host_product = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/processProduct"
hq_host_product_pull = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/receiveProduct"
hq_host_inventory_pull = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/receiveInventory"


class Command(BaseCommand):
    help = 'Local pull of Inventory'

    def handle(self, **options):
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
                    inventory.product_id_id = product_id
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

# To set this up:
# 1. Create file pricing_strategy_cronjob
# 2. In the file, add below line 
# 0 0 * * 0-6 python manage.py recalculate_price 
# (min hr day month day_run Command) << File format, this job runs recalculate_price.py every day at 12am
# 3. On Unix system, run this to set it up: crontab -a pricing_strategy_cronjob                 