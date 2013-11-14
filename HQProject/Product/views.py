# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Product.models import Product, Batch
from Store.models import Store


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
    batches = Batch.objects.filter(product_id_id=id)
    product = Product.objects.get(id=id)
    stores = []
    for b in batches:
        s = Store.objects.get(id=b.store_id_id)
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