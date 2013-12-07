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
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required     
@login_required
def filter_stores(request):
    return render(request,'filter_stores.html')

@staff_member_required    
@login_required
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
    message = 'Click on store ID to view store inventory'
    context = {'stores':stores,'message':message}   
    return render(request, 'view_stores.html',context)

@staff_member_required
@login_required
def view_specific(request,id):
    store = Store.objects.get(store_id=id)
    context = {'store':store}
    return render(request, 'view_specific.html',context)

@staff_member_required
@login_required
def create_store(request):
    return render(request,'create_store.html')

@staff_member_required
@login_required
def store_created(request):
    if 'address' in request.GET and request.GET['address'] and 'city' in request.GET and request.GET['city'] and 'country' in request.GET and request.GET['country'] and 'region' in request.GET and request.GET['region']:
        address = request.GET['address']
        city = request.GET['city']
        country = request.GET['country']        
        if 'city_state' in request.GET:     
            city_state = request.GET['city_state']
        else:
            city_state = city
        region = request.GET['region']
    stores = Store.objects.all().order_by('-store_id')
    if not stores:
        id = 1
    else:
        id = stores[0].store_id+1
    store = Store(store_id=id, address=address,city=city,country=country,state=city_state,region=region)
    store.save() 
    stores = Store.objects.all()
    message = 'Store has been successfully added'
    context = {'stores':stores,'message':message}
    return render(request,'view_stores.html',context)

@staff_member_required
@login_required
def edit_store(request,id):
    store = Store.objects.get(store_id=id)
    context = {'store':store}
    return render(request,'edit_store.html',context)   

@staff_member_required
@login_required
def store_edited(request,id):
    print id
    store = Store.objects.get(store_id=id)
    address = request.GET['address']
    city = request.GET['city']
    country = request.GET['country']        
    state = request.GET['state']
    region = request.GET['region']
    store.address = address
    store.city = city
    store.country = country
    store.state = state
    store.region = region
    store.save()
    stores = Store.objects.all()
    message = 'Store has been successfully edited'
    context = {'stores':stores,'message':message}
    return render(request,'view_stores.html',context)

@staff_member_required    
@login_required
def delete_store(request,id):
    store = Store.objects.get(store_id = id)
    context = {'store':store}
    return render(request,'delete_store.html',context)
    
@staff_member_required     
@login_required
def store_deleted(request,id):
    store = Store.objects.get(store_id=id)
    store.delete()
    batches = Inventory.objects.filter(store_id_id=id)
    batches.delete()
    message = 'Store has been successfully deleted'
    stores = Store.objects.all()
    context = {'stores':stores,'message':message}
    return render(request,'view_stores.html',context)