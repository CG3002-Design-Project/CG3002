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
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 

@login_required
def home_page(request):
	return render(request,'home.html');

