from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction
from decimal import *
from chartit import DataPool, Chart
import random
    
def customer_home(request): 
    return render(request, 'customer_home.html')