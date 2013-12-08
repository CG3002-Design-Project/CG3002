from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction
from django.views.decorators.csrf import csrf_exempt
from decimal import *
import random
import json
    

def cart(request): 
    return render(request, 'cart.html')

def render_map(request): 
    return render(request, 'map_display.html')		
# MUST DO: Either do it here, or create a cron that runs checks on eTrans for a shop's latest pushed qty
# If qty does not exist, create entry in request table (also - should the request update inventory with special status - reserve?)

def order_placed(request):
	if request.user.is_authenticated():
		context = { 'cart_list': cart_list}
		return render(request, 'order_placed.html', context)
	else:
		return render(request, 'login.html')
		
		
def maps(request):
	stores = Store.objects.all()
	list = []
	for s in stores:
		list.append({'store_id':s.store_id,'address':s.address,'city':s.city,'country':s.country})
	payload = {'stores':list}
	data = json.dumps(payload)
	print data;
	return HttpResponse(data,mimetype='application/json')		
	
@csrf_exempt	
def render_storeid(request):
	d =  json.loads(request.body);
	format = d['format']
	a = format.split(",")
	print a[0];
	store = Store.objects.get(address=a[0])
	payload = {'storeid':store.store_id}
	data = json.dumps(payload)
	print data;
	return HttpResponse(data,mimetype='application/json')			