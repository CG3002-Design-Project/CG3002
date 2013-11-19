# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory
from decimal import *
import random

def filter_products(request):
    products = Product.objects.all()
    categories = []
    for p in products:
        if p.category not in categories:
            categories.append(p.category)
    context = {'categories':categories}			
    return render(request,'filter_products.html',context)
   
   
def view_product(request):
    if 'cate' in request.GET and request.GET['cate']:
        category = request.GET['cate']
        if category == 'All':
            products = Product.objects.all()
            c = 'all products'
        else:
            products = Product.objects.filter(category=category)
            c = category
        context = {'products':products,'c':c}
        return render(request, 'view_product.html',context)

		
def add_product(request):
    products = Product.objects.all()
    categories = []
    for p in products:
        if p.category not in categories:
            categories.append(p.category)
    stores = Store.objects.all()	
    context = {'categories':categories,'stores':stores}		
    return render(request,'add_product.html',context)		
		

def product_added(request):
    if 'name' in request.GET and request.GET['name'] and 'manufacturer' in request.GET and request.GET['manufacturer'] and 'cate' in request.GET and request.GET['cate']:
        name = request.GET['name']
        manufacturer = request.GET['manufacturer']
        cate = request.GET['cate']
        if cate == 'Other':
           category = request.GET['category']
        else:
           category = cate
        products = Product.objects.all().order_by('-product_id')
        if not products:
            pid = 1
        else:
            pid = p[0] + 1
        p = Product(product_id=pid, name = name, manufacturer = manufacturer, category = category)
        p.save()
        context = {'product':product}
        return render(request,'product_added.html',product)
		
		
def view_storewise(request,id):
    inventory = Inventory.objects.filter(product_id_id=id)
    product = Product.objects.get(product_id=id)
    stores = []
    for b in batches:
        s = Store.objects.get(store_id=b.store_id_id)
        if s not in stores:
            stores.append(s)
    class s_b:
        def __init__(self):
            self.address = None	
            self.country = None
            self.region = None
            self.minimum_qty = 0
            self.selling_price = 0
            self.qty = 0
            self.expiry_date = None
            self.batch_id = None
            self.store_id = None
    sb = []
    for (s,b) in zip(stores,batches):  
        if s.id == b.store_id_id:
            x = s_b()
            x.address = s.address + ' ' + s.city + ' ' + s.state
            x.country = s.country
            x.region = s.region 			
            x.minimum_qty = b.minimum_qty
            x.selling_price = b.selling_price
            x.qty = b.qty
            x.expiry_date = b.expiry_date
            x.batch_id = b.batch_id
            x.store_id = b.store_id_id
            sb.append(x)			
    context = {'sb':sb,'product':product}
    return render(request, 'view_storewise.html',context)

def filter_stores(request):
   return render(request,'filter_stores.html')
   
   
def view_stores(request):
	if 'region' in request.GET and request.GET['region']:
		region = request.GET['region']
		if 'country' in request.GET and request.GET['country']:
			country = request.GET['country']
			if 'city_state' in request.GET and request.GET['city_state']:
				city_state = request.GET['city_state']
				if 'city' in request.GET and request.GET['city']:
					city = request.GET['city']
					stores = Store.objects.filter(region=region,country=country,state=city_state,city=city)				
				else:
					stores = Store.objects.filter(region=region,country=country,state=city_state)
			else:
				if 'city' in request.GET and request.GET['city']:
					city = request.GET['city']
					stores = Store.objects.filter(region=region,country=country,city=city)
				else:
					stores = Store.objects.filter(region=region,country=country)
		else:
			if 'city' in request.GET and request.GET['city']:
				city = request.GET['city']
				stores = Store.objects.filter(region=region,city=city)
			else:
				stores = Store.objects.filter(region=region)
	else:
		if 'city' in request.GET and request.GET['city']:
			city = request.GET['city']
			stores = Store.objects.filter(city=city)
		else:
			stores = Store.objects.all()	
	context = {'stores':stores}	
	return render(request, 'view_stores.html',context)

def view_specific(request,id):
	store = Store.objects.get(store_id=id)
	context = {'store':store}
	return render(request, 'view_specific.html',context)
	
def inventory_control(request,id):	
    batches = Inventory.objects.filter(store_id_id=id)
    store = Store.objects.get(store_id=id)		
    context = {'batches':batches,'store':store}
    return render(request,'inventory_control.html',context)
	
def search(request,id):
    product_id = request.GET['product_id']
    batches = Inventory.objects.filter(store_id_id=id,product_id_id=product_id)
    store = Store.objects.get(store_id=id)	    
    context = {'batches':batches,'store':store}
    return render(request,'inventory_control.html',context)
	
	
def edit_inventory(request,s_id,b_id,p_id):
    batch = Inventory.objects.get(batch_id=b_id,product_id_id=p_id,store_id_id=s_id)
    store = Store.objects.get(store_id=s_id)
    context = {'batch':batch,'store':store}	
    return render(request,'edit_inventory.html',context)
	
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
	
def inventory_deleted(request,s_id,b_id,p_id): 		
    print b_id 
    print s_id
    print p_id
    batch = Inventory.objects.get(store_id_id=s_id,product_id_id=p_id,batch_id=b_id)
    print batch.batch_id
    batch.delete()
    store = Store.objects.get(store_id=s_id)
    messagedelete = 'Requested inventory row has been deleted'
    batches = Inventory.objects.filter(store_id=s_id)
    context = {'store':store,'messagedelete':messagedelete, 'batches':batches}
    return render(request,'inventory_control.html',context)	

def edit_product(request,sid,pid):
    product = Product.objects.get(product_id=pid)
    store = Store.objects.get(store_id=sid)
    context = {'product':product,'store':store}
    return render(request,'edit_product.html',context)	
	

def product_edited(request,sid,pid):
    product = Product.objects.get(product_id=pid)
    product.name = request.GET['name']
    product.manufacturer = request.GET['manu']
    product.category = request.GET['cate']
    product.save()
    store = Store.objects.get(store_id=sid)
    messageprodupdate = 'The following product has been successfully updated: '
    batches = Inventory.objects.filter(store_id=s_id)
    context = {'product':product,'store':store,'messageprodupdate':messageprodupdate,'batches':batches}
    return render(request,'inventory_control.html',context)	
	

def add_inventory(request,sid):
    store = Store.objects.get(store_id = sid)
    inventory = Inventory.objects.filter(store_id_id = sid)
    productids = []
    for i in inventory:
        if i.product_id_id not in productids:
            productids.append(i.product_id_id)			
    context = {'productids':productids,'store':store}
    return render(request,'add_inventory.html',context)	
    	
		
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
    
		
		
		
def create_product(request,s_id):
    store = Store.objects.get(store_id=s_id)
    context = {'store':store}
    return render(request,'create_product.html',context)	
	
	
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
	
def create_store(request):
    return render(request,'create_store.html')

def store_created(request):
    if 'address' in request.GET and request.GET['address'] and 'city' in request.GET and request.GET['city'] and 'city_state' in request.GET and request.GET['city_state'] and 'country' in request.GET and request.GET['country'] and 'region' in request.GET and request.GET['region']:
        address = request.GET['address']
        city = request.GET['city']
        country = request.GET['country']
        city_state = request.GET['city_state']
        region = request.GET['region']
        store = Store(address=address,city=city,country=country,state=city_state,region=region)
        store.save()
        context = {'store':store}
        return render(request,'view_specific.html',context)
    
def store_deleted(request,id):
    store = Store.objects.get(store_id=id)
    store.delete()
    batches = Inventory.objects.filter(batch_id=id)
    batches.delete()
    message = 'Store has been successfully deleted'
    stores = Store.objects.all()
    context = {'stores':stores,'message':message}
    return render(request,'view_stores.html',context)
	
def edit_store(request,id):
    store = Store.objects.get(id=id)
    context = {'store':store}
    return render(request,'edit_store.html',context)   

def store_edited(request,id):
    store = Store.objects.get(store_id=id)
    if 'address' in request.GET and request.GET['address'] and 'city' in request.GET and request.GET['city'] and 'city_state' in request.GET and request.GET['city_state'] and 'country' in request.GET and request.GET['country'] and 'region' in request.GET and request.GET['region']:
        address = request.GET['address']
        city = request.GET['city']
        country = request.GET['country']		
        state = request.GET['city_state']
        region = request.GET['region']
        store.address = address
        store.city = city
        store.country = country
        store.state = state
        store.region = region
        store.save()
    stores = Store.objects.all()
    edit_message = 'Store has been successfully edited'
    context = {'stores':stores,'edit_message':edit_message}
    return render(request,'view_stores.html',context)	
