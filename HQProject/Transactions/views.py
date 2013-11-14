# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Transactions.models import Transactions
from decimal import *

#https://docs.djangoproject.com/en/1.2/topics/auth/#other-authentication-sources
#http://stackoverflow.com/questions/9825630/login-required-decorator-in-django-1-1-and-template-name

#@login_required(redirect_field_name='my_redirect_field')

#def transactions_home(request):
#   return render(request,'transactions_home.html')

#def add_transaction(request):
#   return render_to_response('add_transaction.html',{},
#       context_instance=RequestContext(request))

def transactions_home(request):
    transactions_list = Transactions.objects.all()
    context = {'transactions_list':transactions_list}
    return render(request, 'transactions_home.html',context)

def add_transaction(request):
    return render_to_response('add_transaction.html',{},
        context_instance=RequestContext(request))

def transactions_added(request):
    if 'transaction_id' in request.GET and request.GET['transaction_id']:
        transaction_id = request.GET['transaction_id']
    else:
        transaction_id = ' '
    if 'cashreg_id' in request.GET and request.GET['cashreg_id']:
        cashreg_id = request.GET['cashreg_id']
    else:
        cashreg_id = 'cashreg_id'
    if 'barcode' in request.GET and request.GET['barcode']:
        barcode = request.GET['barcode']
    else:
        barcode = ' '
    if 'sp' in request.GET and request.GET['sp']:
        sp = request.GET['sp']
    else:
        sp = ' '
    if 'qty' in request.GET and request.GET['qty']:
        qty = request.GET['qty']
    else:
        qty = ' '
    if 'purchase_date' in request.GET and request.GET['purchase_date']:
        purchase_date = request.GET['purchase_date']
    else:
        purchase_date = ' '
            
    new_transaction = Transactions(transaction_id=transaction_id,cashreg_id=cashreg_id,barcode=barcode,qty=qty,sp=sp,purchase_date=purchase_date)
    new_transaction.save()
    return render_to_response('transactions_added.html',{},
        context_instance=RequestContext(request))

def transactions_deleted(request,transaction_id_del,barcode_del):        
    del_transaction = Transactions.objects.get(transaction_id=transaction_id_del,barcode=barcode_del)
    del_transaction.delete()
    context = {'del_transaction':del_transaction}
    return render(request,'transactions_deleted.html',context)  
 
def edit_transactions(request,transaction_id,barcode):
    transactions_list = Transactions.objects.get(transaction_id=transaction_id,barcode=barcode)
    #transactions_list.sp = edited_t.sp
    #transactions_list.cashreg_id = edited_t.cashreg_id
    #transactions_list.qty = edited_t.qty
    #transactions_list.purchase_date = edited_t.purchase_date
    #transactions_list.transaction_id = edited_t.transaction_id
    #transactions_list.barcode = edited_t.barcode
    context = {'transactions_list':transactions_list} 
    return render(request,'edit_transactions.html',context)
    
def transactions_edited(request,transaction_id,barcode):
    if 'cashreg_id' in request.GET and request.GET['cashreg_id']:
        cashreg_id = request.GET['cashreg_id']
    if 'sp' in request.GET and request.GET['sp']:
        sp = request.GET['sp']
    if 'qty' in request.GET and request.GET['qty']:
        qty = request.GET['qty']
    if 'purchase_date' in request.GET and request.GET['purchase_date']:
        purchase_date = request.GET['purchase_date']
     
    transactions_list = Transactions.objects.get(transaction_id=transaction_id,barcode=barcode)
    transactions_list.cashreg_id = cashreg_id
    transactions_list.sp = sp
    transactions_list.qty = qty
    #purchase_date_format = 
    transactions_list.purchase_date = purchase_date
    transactions_list.save()
    context = {'transactions_list':transactions_list}
    return render(request,'transactions_edited.html',context)
