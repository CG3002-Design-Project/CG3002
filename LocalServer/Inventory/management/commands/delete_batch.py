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
        print "hello"
		inventory = inventory.objects.all()
		for i in inventory:
			if (i.qty == 0):
				i.delete();
            
# To set this up:
# 1. Create file pricing_strategy_cronjob
# 2. In the file, add below line 
# 0 0 * * 0-6 python manage.py recalculate_price 
# (min hr day month day_run Command) << File format, this job runs recalculate_price.py every day at 12am
# 3. On Unix system, run this to set it up: crontab -a pricing_strategy_cronjob                 