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
            
# To set this up:
# 1. Create file pricing_strategy_cronjob
# 2. In the file, add below line 
# 0 0 * * 0-6 python manage.py recalculate_price 
# (min hr day month day_run Command) << File format, this job runs recalculate_price.py every day at 12am
# 3. On Unix system, run this to set it up: crontab -a pricing_strategy_cronjob                 