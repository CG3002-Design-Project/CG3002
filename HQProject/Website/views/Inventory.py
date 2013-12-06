from Transaction import *
from Inventory import *
from Restock import *
from Store import *
from Sync import *
from Product import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction, Employee
from decimal import *
from chartit import DataPool, Chart
import random
from django.contrib.auth.models import User
    
@login_required
def inventory_control(request,id):  
    #curr_employee=Employee.objects.get(user_id=request.user.id)
    batches = Inventory.objects.filter(store_id_id=id)
    store = Store.objects.get(store_id=id)      
    #context = {'batches':batches,'store':store,'curr_employee':curr_employee}
    context = {'batches':batches,'store':store}
    return render(request,'inventory_control.html',context)
    
@login_required
def search(request,id):
    product_id = request.GET['product_id']
    batches = Inventory.objects.filter(store_id_id=id,product_id_id=product_id)
    store = Store.objects.get(store_id=id)      
    context = {'batches':batches,'store':store}
    return render(request,'inventory_control.html',context)
    
    
@login_required
def edit_inventory(request,s_id,b_id,p_id):
    batch = Inventory.objects.get(batch_id=b_id,product_id_id=p_id,store_id_id=s_id)
    store = Store.objects.get(store_id=s_id)
    context = {'batch':batch,'store':store} 
    return render(request,'edit_inventory.html',context)
    
@login_required
def inventory_updated(request,s_id,b_id,p_id):  
    if 'product_id' in request.GET and request.GET['product_id'] and 'batch_id' in request.GET and request.GET['batch_id'] and 'qty' in request.GET and request.GET['qty'] and 'cp' in request.GET and request.GET['cp'] and 'sp' in request.GET and request.GET['sp'] and 'minqty' in request.GET and request.GET['minqty']: 
        product_id = request.GET['product_id']
        batch_id = request.GET['batch_id']
        qty = request.GET['qty']
        minqty = request.GET['minqty']
        sp = request.GET['sp']
        cp = request.GET['cp']
    
    if request.GET['ed']:
        ex = request.GET['ed']
        if ex == 'None':
            ex = None
    else:
        ex = None   
    batch = Inventory.objects.get(store_id_id=s_id,product_id_id=p_id,batch_id=b_id)
    batch.qty = qty
    batch.minimum_qty = minqty
    batch.selling_price = sp
    batch.cost_price = cp
    batch.expiry_date = ex
    batch.save()
    messageupdate = 'Inventory has been successfully updated'
    store = Store.objects.get(store_id=s_id)
    batches = Inventory.objects.filter(store_id=s_id)
    context = {'store':store,'batch':batch,'messageupdate':messageupdate,'batches':batches}
    return render(request,'inventory_control.html',context)
	
@login_required
def edit_product(request,sid,pid):
    product = Product.objects.get(product_id=pid)
    store = Store.objects.get(store_id=sid)
    context = {'product':product,'store':store}
    return render(request,'edit_product.html',context)  
    

@login_required
def product_edited(request,sid,pid):
    product = Product.objects.get(product_id=pid)
    product.name = request.GET['name']
    product.manufacturer = request.GET['manu']
    product.category = request.GET['cate']
    product.save()
    store = Store.objects.get(store_id=sid)
    message = 'Product has been successfully updated'
    batches = Inventory.objects.filter(store_id=s_id)
    context = {'product':product,'store':store,'message':message,'batches':batches}
    return render(request,'inventory_control.html',context) 
    

@login_required
def add_inventory(request,sid):
    products = Product.objects.all()    
    productids = []
    for p in products:
        productids.append(p.product_id)
    store = Store.objects.get(store_id=sid)
    context = {'productids':productids,'store':store}
    return render(request,'add_inventory.html',context) 
        
        
@login_required
def inventory_added(request,sid):
    if 'product_id' in request.GET and request.GET['product_id'] and 'qty' in request.GET and request.GET['qty'] and 'cp' in request.GET and request.GET['cp'] and 'sp' in request.GET and request.GET['sp'] and 'minqty' in request.GET and request.GET['minqty']: 
        product_id = request.GET['product_id']
        qty = request.GET['qty']
        minqty = request.GET['minqty']
        sp = request.GET['sp']
        cp = request.GET['cp']
    if request.GET['ed']:
        ex = request.GET['ed']
    else:
        ex=None
    inv = Inventory.objects.filter(store_id=sid,product_id_id=product_id)
    batchid = random.randint(1,99999)
    ids = []
    for i in inv:
        ids.append(i.batch_id)
        while(batchid in ids):
            batchid = random.randint(1,99999)
    batch = Inventory(product_id_id=product_id,batch_id=batchid,store_id_id=sid,qty=qty,minimum_qty=minqty,selling_price=sp,cost_price=cp,expiry_date=ex)
    batch.save()
    messageadd = 'New inventory has been successfully added'
    store = Store.objects.get(store_id=sid)
    batches = Inventory.objects.filter(store_id=sid)
    context = {'store':store,'messageadd':messageadd,'batches':batches}
    return render(request,'inventory_control.html',context)

@login_required
def delete_inventory(request,sid,bid,pid):
    inv = Inventory.objects.get(store_id_id=sid,product_id_id=pid,batch_id=bid)
    context = {'inv':inv}
    return render(request,'delete_inventory.html',context)    

@login_required
def inventory_deleted(request,sid,bid,pid):
    inv = Inventory.objects.get(store_id_id=sid,product_id_id=pid,batch_id=bid)
    inv.delete()
    batches = Inventory.objects.all()
    store = Store.objects.get(store_id=sid)
    messagedelete = 'Requested inventory row has been deleted'
    context = {'store':store,'batches':batches,'messagedelete':messagedelete}
    return render(request,'inventory_control.html',context)


