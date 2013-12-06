from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction
from decimal import *
from chartit import DataPool, Chart
import random
    
def cart(request): 
    return render(request, 'cart.html')

# MUST DO: Either do it here, or create a cron that runs checks on eTrans for a shop's latest pushed qty
# If qty does not exist, create entry in request table (also - should the request update inventory with special status - reserve?)

def order_placed(request):
	context = {}
	if 'store_id' in request.GET and request.GET['store_id'] and 'p_id_1' in request.GET and request.GET['p_id_1'] and 'b_id_1' in request.GET and request.GET['b_id_1'] and 'qty_1' in request.GET and request.GET['qty_1'] and 'p_id_2' in request.GET and request.GET['p_id_2'] and 'b_id_2' in request.GET and request.GET['b_id_2']  and 'qty_2' in request.GET and request.GET['qty_2'] and 'p_id_3' in request.GET and request.GET['p_id_3']  and 'b_id_3' in request.GET and request.GET['b_id_3'] and 'qty_3' in request.GET and request.GET['qty_3']:
		store_id = request.GET['store_id']
		p_id_1 = request.GET['p_id_1']
		qty_1 = request.GET['qty_1']
		b_id_1 = request.GET['b_id_1']
		p_details_1 = Inventory.objects.get(store_id=store_id,product_id=p_id_1,batch_id=b_id_1) 
		cost_price_1 = p_details_1.cost_price
		selling_price_1 = p_details_1.selling_price

		p_id_2 = request.GET['p_id_2']
		qty_2 = request.GET['qty_2']
		b_id_2 = request.GET['b_id_2']
		p_details_2 = Inventory.objects.get(store_id=store_id,product_id=p_id_2,batch_id=b_id_2) 
		cost_price_2 = p_details_2.cost_price
		selling_price_2 = p_details_2.selling_price

		p_id_3 = request.GET['p_id_3']
		qty_3 = request.GET['qty_3']
		b_id_3 = request.GET['b_id_3']
		p_details_3 = Inventory.objects.get(store_id=store_id,product_id=p_id_3,batch_id=b_id_3) 
		cost_price_3 = p_details_3.cost_price
		selling_price_3 = p_details_3.selling_price

		et_list = Transaction.objects.all().order_by('-transaction_id');
		if not et_list:
			transaction_id = 1;
		else:
			transaction_id = et_list[0].transaction_id+1;
		et_1 = eTransaction(store_id=store_id, transaction_id= transaction_id, transaction_date = time.strftime("%Y-%m-%d"), product_id = i['p_id_1'], quantity_sold = i['qty_1'], batch_id = i['b_id_1'], status = "Placed", cost_price=cost_price_1, selling_price=selling_price_1)
		et_1.save()
		et_2 = eTransaction(store_id=store_id, transaction_id= transaction_id, transaction_date = time.strftime("%Y-%m-%d"), product_id = i['p_id_2'], quantity_sold = i['qty_2'], batch_id = i['b_id_2'], status = "Placed", cost_price=cost_price_2, selling_price=selling_price_2)
		et_2.save()
		et_3 = eTransaction(store_id=store_id, transaction_id= transaction_id, transaction_date = time.strftime("%Y-%m-%d"), product_id = i['p_id_3'], quantity_sold = i['qty_3'], batch_id = i['b_id_3'], status = "Placed", cost_price=cost_price_3, selling_price=selling_price_3)
		et_3.save()
		context = { 'et_1': et_1}
	return render(request, 'order_placed.html', context)