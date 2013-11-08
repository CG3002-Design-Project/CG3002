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
