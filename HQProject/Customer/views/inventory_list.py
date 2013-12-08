from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction
from decimal import *
from random import choice
import random
    
imageid_list = [10844205, 12289374, 12494366, 12609068, 12628600, 13750311, 13807078, 14673458, 15016920, 15069368, 15563048, 18355734, 18417740, 18603250, 19352766, 19619262, 20151308, 20219909, 21509673, 22016225, 23418003,23923790, 24002185, 25959259, 26398554,27067231, 27104807, 29170545, 29437606, 29478162, 29614923, 30617200, 31555897, 32100416, 32315143, 32407804, 33995417, 34210032, 34571368, 35017012, 37189238, 37461060, 37507164, 37896204, 38545539, 40155785, 44666193, 44816930, 47915380, 48933685, 50599972, 51052198, 52044496, 54053173, 54115988, 54815480, 55164183, 56053688, 58816051, 59030623, 59416143, 60340214, 61187597, 61355704, 61424341, 63842248, 66209379, 66335976, 66752080, 67483318, 67620416, 68504798, 68626387, 68985378, 69849369, 71450867, 73894790, 75013426, 75676122, 77797546, 78339711, 79310608, 80631015, 82139223, 83383140, 84051612, 85000937, 85972997]
	
def inventory_list(request):
	class inven_prod:
		def __init__(self):
			self.name = None
			self.productid = None			
			self.category = None
			self.description = None
			self.imageid = None
			self.cost_price = 0
			self.rating = 0
			self.selling_price = 0
		   
	inventory = Inventory.objects.filter(store_id=5);
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
			obj.selling_price = i.selling_price
			obj.cost_price = i.cost_price
			obj.batchid = i.batch_id
			obj.rating = random.randrange(1,6)
			if obj.productid not in imageid_list:
				print "hello"
				obj.imageid = random.choice(imageid_list)
			else:
				obj.imageid = product
			object_list.append(obj)		
		
	context = {'inventory':object_list} 			
	return render(request, 'inventory_list.html',context)
	
	