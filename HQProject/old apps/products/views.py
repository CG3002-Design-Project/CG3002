# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from products.models import Products,Store


def search_form(request):
    stores = Store.objects.all()
    return render_to_response('search_form.html',{'stores':stores}, context_instance=RequestContext(request))


def search(request):
    if 'name' in request.GET and request.GET['name']:
	name = request.GET['name']
	manufacturer = request.GET['manufacturer']
	p = Products(name=name,manufacturer=manufacturer) 
	p.save()
