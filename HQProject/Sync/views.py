# Create your views here.

# Create your views herefrom django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction,RequestDetails
from Customer.models import eTransaction
import json
import random
import datetime
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from decimal import *
shop_transaction = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/Shop/"

@csrf_exempt
def localPushInventory(request):
    data=json.loads(request.raw_post_data)
    inventory =data['inventory']
    for i in inventory:
        batchid = int(i['batchid'])
        productid=int(i['product_id'])
        qty = int(i['qty'])
        minimum_qty = int(i['minimum_qty'])
        selling_price = Decimal(i['selling_price'])
        shopid = int(i['shopid'])
        inv = Inventory.objects.get(product_id_id=productid,batch_id=batchid,store_id_id=1)
        inv.qty = qty
        inv.selling_price = selling_price
        inv.minimum_qty = minimum_qty
        inv.save()
	
	eTran  = eTransaction.objects.all();
	for e in eTran:
		inv = Inventory.objects.get(store_id_id=e.store_id,product_id_id=e.product_id,batch_id=e.batch_id);
		if(inv.qty < e.quantity_sold):
			r = RequestDetails.objects.all().order_by('-request_id');
			if not r:
				request_id = 1;
			else:
				request_id = r[0].request_id+1;
			r = RequestDetails(request_id=request_id,request_date = e.transaction_date, qty = e.quantity_sold, store_id=e.store_id,product_id=e.product_id,status='reserved')
			r.save();
	return HttpResponse('yo')


@csrf_exempt
def localPushProduct(request):
    data = json.loads(request.raw_post_data)
    product = data['product']
    for p in product:
        product_id = int(p['product_id'])
        min_restock = int(p['min_restock'])
        shopid = int(p['shopid'])
        name = p['name']
        manufacturer = p['manufacturer']
        category = p['category']
        product = Product.objects.get(product_id=product_id)
        product.name = name
        product.category = category
        product.manufacturer = manufacturer		
        product.min_restock = min_restock
        product.save()  
    return HttpResponse('Yo')      

		
@csrf_exempt
def localPushTransaction(request):
    data=json.loads(request.raw_post_data)
    transaction = data['transaction']
    for i in transaction:
        transaction_id =  int(i['transaction_id'])
        transaction_date = datetime.datetime.strptime(i['transaction_date'], '%Y-%m-%d').date()
        cashreg_id =  int(i['cashregid'])
        barcode =  int(i['barcode'])
        qty = int(i['qty'])
        shopid = int(i['shopid'])
        selling_price =  Decimal(i['selling_price'])
        cost_price = Decimal(i['cost_price'])
        batchid = int(i['batchid'])
    	new_transaction = Transaction(transaction_id=transaction_id,transaction_date = transaction_date, cashier_id = cashreg_id, store_id=shopid,product_id = barcode, quantity_sold=qty,selling_price=selling_price,cost_price=cost_price,batch_id=batchid)
    	new_transaction.save()	
    return HttpResponse('Yo Transaction')

@csrf_exempt
def localPushRequests(request):
    data= json.loads(request.raw_post_data)
    rd = data['request_details']
    for i in rd:
        qty =  int(i['qty'])
        request_id = int(i['request_id'])
        product_id =  int(i['product_id'])
        request_date = datetime.datetime.strptime(i['request_date'], '%Y-%m-%d').date()
        shopid = int(i['shopid'])
        new_request = RequestDetails(request_id=request_id,request_date = request_date, qty = qty, store_id=shopid,product_id=product_id,status='received')
        new_request.save()	
    return HttpResponse('Yo request')

@csrf_exempt
def localPullInventory(request):
    store = request.GET['shopid']
    requests_sent = RequestDetails.objects.filter(store_id=store)
    for r in requests_sent:
        inv = Inventory.objects.filter(product_id_id=r.product_id,store_id_id=store)        
        batchid = random.randint(1,99999)
        ids = []
        for i in inv:
            ids.append(i.batch_id)
        while(batchid in ids):
                batchid = random.randint(1,99999)
        batches = Inventory.objects.filter(product_id_id = r.product_id, store_id_id = store).order_by('-batch_id')
        newbatch = Inventory(product_id_id=r.product_id,store_id_id=store,batch_id=batchid,qty = r.qty,selling_price = batches[0].selling_price, cost_price=batches[0].cost_price, minimum_qty = batches[0].minimum_qty, expiry_date=batches[0].expiry_date)
        newbatch.save()
        r.delete()
    inventory = Inventory.objects.filter(store_id_id=store)     
    if(inventory is not None):
        list = []
        for i in inventory:
            list.append({'qty' : str(i.qty), 
                         'batchid' : str(i.batch_id),
                         'productid': str(i.product_id_id),
                         'minimum_qty': str(i.minimum_qty),
                         'selling_price' : str(i.selling_price),
                         'cost_price' : str(i.cost_price),
                         'minimum_qty': str(i.minimum_qty),
                         'expiry_date': str(i.expiry_date)}) 
	
	payload = { 'inventory': list }
    data = json.dumps(payload)
    return HttpResponse(data, content_type="application/json")					 

@csrf_exempt	
def localPullETransaction(request):
	store = request.GET['shopid']
	etran = eTransaction.objects.filter(store_id=store); 
	list2 =[]
	for e in etran:
		list2.append({'transaction_id' : str(e.transaction_id), 
					 'transaction_date' : str(e.transaction_date),
					 'product_id': str(e.product_id),
					 'quantity_sold': str(e.quantity_sold),
					 'batch_id' : str(e.batch_id),
					 'selling_price' : str(e.selling_price),
					 'cost_price': str(e.cost_price),
					 'status': str(e.status)}) 
		
	payload = { 'etran': list2 }
	data = json.dumps(payload)
	return HttpResponse(data, content_type="application/json")

    
@csrf_exempt
def localPullProduct(request):
    store = request.GET['shopid'] 
    inv = Inventory.objects.filter(store_id_id=store)
    products = []
    list = []
    for i in inv:
        if (i.product_id_id not in products):
            products.append(i.product_id_id)
    for pr in products:
        p = Product.objects.get(product_id=pr)          
        list.append({'name' : (p.name),
                         'manufacturer' : (p.manufacturer),
                         'product_id': str(p.product_id),
                         'category': (p.category),
                         'min_restock': str(p.min_restock),
                         'status': (p.status)})
    payload = {'product': list}
    data = json.dumps(payload)
    return HttpResponse(data, content_type="application/json")
    

#ders = {'content-type': 'application/json'}
#def sync_function(request):
 #   store_list = Store.objects.all();
  #  for store_sync in store_list:
   #     transaction_list = Transaction.objects.get(store_id=store_sync.store_id)
    #    if(transaction_list is not None):
     #       list = []
      #      for i in transaction_list:
       #          list.append({'transaction_id': str(i.transaction_id),
        #                     'cashier_id' : str(cashid), 
         #                    'product_id':str(i.product_id),
          #                   'quantity_sold': str(i.quantity_sold), 
           #                  'batch_id': str(10), 
            #                 'transaction_date':str(i.transaction_date),
             #                'cost_price': str(cost_price),
              #               'selling_price': str(selling_price)})
           # payload = {
            #        'store_id': store_sync_id,   
             #       'transaction':list
           # }
           # data = json.dumps(payload)
           # headers = {'content-type': 'application/json'}
           # res = requests.post(shop_transaction + store_sync_id,data,headers = headers)
           # return render(request,'sync_function.html');
