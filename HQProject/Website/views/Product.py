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
from Website.models import Store,Product,Inventory,Transaction
from decimal import *
import random
    
@login_required
def filter_products(request):
    products = Product.objects.all()
    categories = []
    for p in products:
        if p.category not in categories:
            categories.append(p.category)
    context = {'categories':categories}         
    return render(request,'filter_products.html',context)
   
   
@login_required
def view_product(request):
    products = Product.objects.all()
    message = 'Click on Product ID to view storewise inventory'    
    context = {'products':products,'message':message}
    return render(request,'view_product.html',context)


@login_required
def add_product(request):
    products = Product.objects.all()
    categories = []
    for p in products:
        if p.category not in categories:
            categories.append(p.category)
    stores = Store.objects.all()    
    context = {'categories':categories,'stores':stores}     
    return render(request,'add_product.html',context)       
        

@login_required
def product_added(request):
    if 'name' in request.GET and request.GET['name'] and 'manufacturer' in request.GET and request.GET['manufacturer'] and 'cate' in request.GET and request.GET['cate'] and 'minrestock' in request.GET and request.GET['minrestock']:
        name = request.GET['name']
        manufacturer = request.GET['manufacturer']
        cate = request.GET['cate']
        minrestock = request.GET['minrestock']
        if cate == 'Other':
           category = request.GET['category']
        else:
           category = cate
        products = Product.objects.all().order_by('-product_id')
        if not products:
            pid = 1
        else:
            pid = products[0].product_id + 1
        p = Product(product_id=pid, name = name, manufacturer = manufacturer, category = category, min_restock = minrestock)
        p.save()
        pr = p 
        products = Product.objects.all()
        message = 'The following product has been successfully added. '
        context = {'pr':pr,'message':message,'products':products}
        return render(request,'view_product.html',context)
        
@login_required
def delete_product(request,id):
    product = Product.objects.get(product_id=id)
    context = {'product':product}
    return render(request,'delete_product.html',context)
        
@login_required
def product_deleted(request,id):
    product = Product.objects.get(product_id=id)
    inv = Inventory.objects.filter(product_id_id=id)
    for i in inv:
        i.selling_price = i.selling_price * Decimal(0.5)
        i.save()    
    product.status = 'Discontinued'
    product.save()
    products = Product.objects.all()    
    message = 'Product has been successfully discontinued '
    context = {'product':product,'products':products,'messagedelete':messagedelete}
    return render(request,'view_product.html',context)  
            
        
@login_required
def view_storewise(request,id):
    product = Product.objects.get(product_id=id)
    inventory = Inventory.objects.filter(product_id=id)
    stores = []
    for i in inventory:     
        store = Store.objects.get(store_id=i.store_id_id) 
        stores.append(store)
    list = zip(stores, inventory)       
    context = {'list':list,'product':product}
    return render(request, 'view_storewise.html',context)

@login_required
def create_product(request,s_id):
    store = Store.objects.get(store_id=s_id)
    context = {'store':store}
    return render(request,'create_product.html',context)    
    
    
@login_required
def product_created(request,s_id):
    store = Store.objects.get(store_id=s_id)
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
    else:
        name = ' '
    if 'manufacturer' in request.GET and request.GET['manufacturer']:
        manufacturer = request.GET['manufacturer']
    else:
        manufacturer = ' '
    if 'category' in request.GET and request.GET['category']:
        category = request.GET['category']
    else:
        category = ' '
    if 'minqty' in request.GET and request.GET['minqty']:
        minqty = request.GET['minqty']
    else:
        minqty=' '
    if 'sp' in request.GET and request.GET['sp']:
        sp = request.GET['sp']
    else:
        sp = ' '
    
    if 'stock' in request.GET and request.GET['stock']:
        qty = request.GET['stock']
    else:
        qty = ' '
        
    if 'ed' in request.GET and request.GET['ed']: 
        ed = request.GET['ed']          
    else:
        ed = ' '    
            
    product = Product.objects.filter(name=name,manufacturer=manufacturer,category=category)
    if not product:
        pr = Product(name=name,manufacturer=manufacturer,category=category)
        pr.save()
        pid = pr.id
    else:
        pid = product[0].id    
    e_d = ed.replace('-','')        
    p_id = str(pid)
    x = p_id + e_d  
    b_id = Decimal(x) 
    batch = Batch(store_id_id=s_id,product_id_id=pid,minimum_qty=minqty,qty=qty,selling_price=sp,expiry_date=ed,batch_id=b_id)
    batch.save()
    store = Store.objects.get(id=s_id)
    p = Product.objects.get(id=pr.id)
    context = {'store':store,'p':p}
    return render(request,'product_created.html',context)		
	

