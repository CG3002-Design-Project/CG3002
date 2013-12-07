from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction
from decimal import *
import random
    
cart_list = []

def cart(request): 
    return render(request, 'cart.html')

# MUST DO: Either do it here, or create a cron that runs checks on eTrans for a shop's latest pushed qty
# If qty does not exist, create entry in request table (also - should the request update inventory with special status - reserve?)

def order_placed(request):
	if request.user.is_authenticated():
		context = { 'cart_list': cart_list}
		return render(request, 'order_placed.html', context)
	else:
		return render(request, 'login.html')