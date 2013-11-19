import django_tables2 as tables
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Inventory.models import Inventory, RequestDetails
from Inventory.models import Product
from Inventory.models import Transaction
from datetime import date
from decimal import *
from django.views.decorators.csrf import csrf_exempt
import json
import os
import time
import serial


class ProductTable(tables.Table):
    class Meta:
        model = Product
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}