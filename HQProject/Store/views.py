# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from Store.models import Store


def store_mainpage(request):
    return render(request,'store_mainpage.html')

def create_store(request):
	return render(request,'create_store.html')
	
	
def created_store(request):
	if 'addr1' in request.GET and request.GET['addr1'] and 'addr2' in request.GET and request.GET['addr2'] and 'city' in request.GET and request.GET['city'] and 'state' in request.GET and request.GET['state'] and 'country' in request.GET and request.GET['country']:
		addr1 = request.GET['addr1']
		addr2 = request.GET['addr2']
		address = addr1 + ' ' + addr2
		city = request.GET['city']
		state = request.GET['state']
		country = request.GET['country']
		region = request.GET['region']
		store = Store(address=address,city=city,state=state,country=country,region=region)
		store.save()
		return HttpResponse("Store created successfully")

def update_store(request):
	return render(request,'update_store.html')
	
def view_stores(request):
	if 'region' in request.GET and request.GET['region'] and 'country' in request.GET and request.GET['country'] and 'city' in request.GET and request.GET['city']:
		region = request.GET['region']
		country = request.GET['country']
		city = request.GET['city']
		stores = Store.objects.filter(region=region,country=country,city=city)
		context = {'stores':stores}	
		return render(request, 'view_stores.html',context)
						
def updated_store(request):
	#if 'address' in request.GET and request.GET['address']:
	#	address = address
		
	#	s = Store(address=address)		
	return HttpResponse("Bye")