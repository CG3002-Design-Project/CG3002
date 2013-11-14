# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction
from decimal import *

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
    class product_batch:
        def __init__(self):
            self.name = None
            self.manufacturer = None
            self.category = None	
            self.minimum_qty = 0
            self.selling_price = 0
            self.qty = 0
            self.expiry_date = None
            self.product_id = None
            self.batch_id = None
            self.store_id = None   
    store = Store.objects.get(store_id=id)

    batches = Inventory.objects.filter(store_id_id=store.id)
    products = []
    p_b = []
    for b in batches:	
        products.append(Product.objects.get(product_id=b.product_id_id))	
			
    for (p,b) in zip(products,batches):
        if b.product_id_id == p.id:
            x = product_batch()
            x.name = p.name
            x.manufacturer = p.manufacturer
            x.category = p.category
            x.minimum_qty = b.minimum_qty
            x.selling_price = b.selling_price
            x.qty = b.qty
            x.expiry_date = b.expiry_date
            x.product_id = b.product_id_id
            x.batch_id = b.batch_id
            x.store_id = b.store_id_id
            p_b.append(x)	
    context = {'p_b':p_b,'store':store}
    return render(request,'inventory_control.html',context)
	
def edit_product(request,s_id,b_id,p_id):
    class product_batch:
        def __init__(self):
            self.name = None
            self.manufacturer = None
            self.category = None	
            self.minimum_qty = 0
            self.selling_price = 0
            self.qty = 0
            self.expiry_date = None
            self.product_id = None
            self.batch_id = None
            self.store_id = None
    product = Product.objects.get(product_id=p_id)
    batch = Inventory.objects.get(batch_id=b_id,product_id_id=p_id,store_id_id=s_id)
    store = Store.objects.get(id=s_id)
    p_b = product_batch()	
    p_b.name = product.name
    p_b.manufacturer = product.manufacturer
    p_b.category = product.category
    p_b.minimum_qty = batch.minimum_qty
    p_b.selling_price = batch.selling_price
    p_b.qty = batch.qty
    p_b.expiry_date = batch.expiry_date
    p_b.product_id = batch.product_id_id
    p_b.batch_id = batch.batch_id
    p_b.store_id = batch.store_id_id
    context = {'p_b':p_b,'store':store}	
    return render(request,'edit_product.html',context)
	
def product_updated(request,s_id,b_id,p_id):
    if 'name' in request.GET and request.GET['name'] and 'manufacturer' in request.GET and request.GET['manufacturer'] and 'category' in request.GET and request.GET['category'] and 'minqty' in request.GET and request.GET['minqty'] and 'sp' in request.GET and request.GET['sp'] and 'stock' in request.GET and request.GET['stock'] and 'ed' in request.GET and request.GET['ed']: 
        name = request.GET['name']
        manufacturer = request.GET['manufacturer']
        category = request.GET['category']
        minqty = request.GET['minqty']
        sp = request.GET['sp']
        qty = request.GET['stock']
        ed = request.GET['ed']
		
    p_b = Batch.objects.get(store_id_id=s_id,product_id_id=p_id,batch_id=b_id)
    p_b.minimum_qty = minqty
    p_b.selling_price = sp
    p_b.qty = qty
    if ed != 'None':
        p_b.expiry_date = ed
    p_b.save()
    p = Product.objects.get(id=p_id)
    p.name = name
    p.manufacturer = manufacturer
    p.category = category
    p.save()	
    store = Store.objects.get(id=s_id)
    context = {'store':store,'p':p}
    return render(request,'product_updated.html',context)
	
def product_deleted(request,s_id,b_id,p_id): 		
    batch = Batch.objects.get(store_id_id=s_id,product_id_id=p_id,batch_id=b_id)
    batch.delete()
    store = Store.objects.filter(id=s_id)
    p = Product.objects.get(id=p_id)
    context = {'store':store,'p':p}
    return render(request,'product_deleted.html',context)	

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

def transaction_home(request):
    transaction_list = Transaction.objects.all()
    context = {'transaction_list':transaction_list}
    return render(request, 'transaction_home.html',context)

def add_transaction(request):
    return render_to_response('add_transaction.html',{},
        context_instance=RequestContext(request))

def transaction_added(request):
    if 'transaction_id' in request.GET and request.GET['transaction_id']:
        transaction_id = request.GET['transaction_id']
    else:
        transaction_id = ' '
    if 'cashier_id' in request.GET and request.GET['cashier_id']:
        cashier_id = request.GET['cashier_id']
    else:
        cashier_id = ' '
    if 'store_id' in request.GET and request.GET['store_id']:
        store_id = request.GET['store_id']
    else:
        store_id = ' '
    if 'product_id' in request.GET and request.GET['product_id']:
        product_id = request.GET['product_id']
    else:
        product_id = ' '
    if 'quantity_sold' in request.GET and request.GET['quantity_sold']:
        quantity_sold = request.GET['quantity_sold']
    else:
        quantity_sold = ' '
    if 'selling_price' in request.GET and request.GET['selling_price']:
        selling_price = request.GET['selling_price']
    else:
        selling_price = ' '
    if 'transaction_date' in request.GET and request.GET['transaction_date']:
        transaction_date = request.GET['transaction_date']
    else:
        transaction_date = ' '
    if 'batch_id' in request.GET and request.GET['batch_id']:
        batch_id = request.GET['batch_id']
    else:
        batch_id = ' '
         
    new_transaction = Transaction(transaction_id=transaction_id, store_id=store_id, transaction_date=transaction_date, product_id=product_id, quantity_sold=quantity_sold, batch_id=batch_id, cashier_id=cashier_id, selling_price=selling_price)
    new_transaction.save()
    return render_to_response('transaction_added.html',{},
        context_instance=RequestContext(request))

def transaction_deleted(request,transaction_id_del,product_id_del):        
    del_transaction = Transaction.objects.get(transaction_id=transaction_id_del,product_id=product_id_del)
    del_transaction.delete()
    context = {'del_transaction':del_transaction}
    return render(request,'transaction_deleted.html',context)  
 
def edit_transaction(request,transaction_id,product_id):
    transaction_list = Transaction.objects.get(transaction_id=transaction_id,product_id=product_id)
    context = {'transaction_list':transaction_list} 
    return render(request,'edit_transaction.html',context)
       
def transaction_edited(request,transaction_id,product_id):
    if 'cashier_id' in request.GET and request.GET['cashier_id']:
        cashier_id = request.GET['cashier_id']
    if 'store_id' in request.GET and request.GET['store_id']:
        store_id = request.GET['store_id']
    if 'quantity_sold' in request.GET and request.GET['quantity_sold']:
        quantity_sold = request.GET['quantity_sold']
    if 'selling_price' in request.GET and request.GET['selling_price']:
        selling_price = request.GET['selling_price']
    if 'transaction_date' in request.GET and request.GET['transaction_date']:
        transaction_date = request.GET['transaction_date']
    if 'batch_id' in request.GET and request.GET['batch_id']:
        batch_id = request.GET['batch_id']
     
    transaction_list = Transaction.objects.get(transaction_id=transaction_id,product_id=product_id)
    transaction_list.cashier_id = cashier_id
    transaction_list.selling_price = selling_price
    transaction_list.quantity_sold = quantity_sold
    transaction_list.transaction_date = transaction_date
    transaction_list.batch_id = batch_id
    transaction_list.store_id = store_id
    transaction_list.save()
    context = {'transaction_list':transaction_list}
    return render(request,'transaction_edited.html',context)



