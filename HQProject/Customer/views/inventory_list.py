from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction
from decimal import *
import random
    
def inventory_list(request):
	class inven_prod:
		def __init__(self):
			self.name = None
			self.productid = None			
			self.category = None
			self.description = None
			self.price = 0
			self.rating = 0
		   
	inventory = Inventory.objects.filter(store_id=1);
	object_list = []   
	for i in inventory:
		product = i.product_id_id
		product_obj = Product.objects.get(product_id=product)
		if i.batch_id == 2:
			obj = inven_prod();
			obj.productid = product
			obj.name = product_obj.name
			obj.category = product_obj.category
			obj.description = "test"
			obj.price = i.selling_price
			obj.batchid = i.batch_id
			obj.rating = 12345
			object_list.append(obj)		
		
	context = {'inventory':object_list} 			
	return render(request, 'inventory_list.html',context)
	
	