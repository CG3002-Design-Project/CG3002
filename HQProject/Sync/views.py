# Create your views herefrom django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Store.models import Store
from Transactions.models import Transactions
from Product.models import Product, Batch
import json
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from decimal import *
shop_transaction = "http://ec2-user@ec2-54-254-157-48.ap-southeast-1.compute.amazonaws.com:8000/Sync/Shop/"

@csrf_exempt
def process(request):
    data=json.loads(request.raw_post_data)
    shopid=data['shopid']
    inventory =data['inventory']
    for i in inventory:
        batchid = Decimal(i['batchid'])
        productid=Decimal(i['product_id'])
        qty= Decimal(i['qty'])
        batch = Batch.objects.get(product_id_id=productid,store_id_id=shopid,batch_id=batchid)
        batch.qty = qty
        batch.expiry_date = '2013-10-10'
        batch.save()    
    return HttpResponse('Yo')      

@csrf_exempt
def processT(request):
    print "ello"
    data=json.loads(request.raw_post_data)
    shopid=data['shopid']
    transaction =data['transaction']
    print transaction[0]
    for i in transaction:
        transaction_id =  Decimal(i['transactionid'])
        cashreg_id =  Decimal(i['cashregid'])
        barcode =  Decimal(i['barcode'])
        qty =  Decimal(i['qty'])
        sp =  Decimal(i['sp'])
        purchase_date = i['purchasedate']
       # shop_id = i['shopid']
    	new_transaction = Transactions(transaction_id=transaction_id,shop_id=shopid,cashreg_id=cashreg_id,barcode=barcode,qty=qty,sp=sp,purchase_date=purchase_date)
    	new_transaction.save()	
    return HttpResponse('Yo Transaction')

def local_transaction_sync(request,store_sync_id):
    store_list = Store.objects.all();
    for store_sync_id in store_list:
        transaction_list = Transaction.objects.get(store_id=store_sync_id)
        if(transaction_list is not None):
            list = []
            for i in transaction_list:
                 list.append({'transaction_id': str(i.transaction_id),
                             'cashier_id' : str(cashid), 
                             'product_id':str(i.product_id),
                             'quantity_sold': str(i.quantity_sold), 
                             'batch_id': str(10), 
                             'transaction_date':str(i.transaction_date), 
                             'selling_price': str(selling_price)})
            payload = {
                    'store_id': store_sync_id,   
                    'transaction':list
            }
            data = json.dumps(payload)
            headers = {'content-type': 'application/json'}
            res = requests.post(shop_transaction + store_sync_id,data,headers = headers)
            return render(request,'sync_function.html');