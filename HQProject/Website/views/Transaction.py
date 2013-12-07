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
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader, RequestContext
from django.db.models import Avg, Sum
from Website.models import Store,Product,Inventory,Transaction
from chartit import DataPool, PivotDataPool, Chart, PivotChart
from decimal import *
from operator import itemgetter
import random
import json
from datetime import date
import operator

@login_required
def transaction_home(request):
	transaction_list = Transaction.objects.all()
	context = {'transaction_list':transaction_list}
	return render(request, 'transaction_home.html',context)

@csrf_exempt	
def top_ten_products_old(request):
	store =  Store.objects.all()
	output = []
	for s in store:
		if s.store_id not in output:
			output.append(s.store_id)
	print output			
	context = {'storeid':output}  
	return render (request,'top_tenProducts.html',context)

@csrf_exempt
def top_ten_products(request):
	#d =  json.loads(request.body)
	#if d['storeid'] is None:
	#	storeid = 1;
	#else:
	print "here"
	if 'store_selected' in request.GET and request.GET['store_selected']:
		store_selected = request.GET['store_selected']
		print store_selected;
	else:
		store_selected = "All"

	if (store_selected=="All"):
		transaction_list= Transaction.objects.all()
	else:
		transaction_list= Transaction.objects.filter(store_id=store_selected)

	store_list =  Store.objects.all()
	productrevenue = \
        PivotDataPool(
          series=
            [{'options': {
               'source': transaction_list,
               'categories' : ['product_id']},
              'terms': {
                'avg_revenue': Avg('selling_price')}}],
                #'top_n' : 10}}]
          top_n = 10,
          top_n_term = 'avg_revenue')
	
	transaction_stats = \
        PivotChart(
            datasource = productrevenue,
            series_options =
              [{'options':{
                  'type': 'column',
                  'stacking': True},
                'terms':[
                    'avg_revenue']
                  }],
            chart_options =
              {'title': {
                   'text': 'Revenue by Product'},
               'xAxis': {
                    'title': {
                       'text': 'Product ID'}}})


					   
	return render(request,'top_tenProducts.html',
                    {
                        'transaction_stats': transaction_stats,
                        'store_list' : store_list

                    }
                )	
@csrf_exempt	
def monthly_stats(request):
	#d =  json.loads(request.body)
	#if d['storeid'] is None:
	#	storeid = 1;
	#else:
	print "here"
	if 'store_selected' in request.GET and request.GET['store_selected']:
		store_selected = request.GET['store_selected']
		print store_selected;
	else:
		store_selected = "All"

	if (store_selected=="All"):
		transaction_list= Transaction.objects.all()
	else:
		transaction_list= Transaction.objects.filter(store_id=store_selected)

	store_list =  Store.objects.all()
#	transaction_list = Transaction.objects.filter(store_id=1)
#	transaction_list = Transaction.objects.all()
	dateRevenue = \
		PivotDataPool(
          series=
            [{'options': {
               'source': transaction_list,
               'categories' : ['transaction_date']},
              'terms': {
                'avg_revenue': Avg('selling_price')}}])
	
	transaction_stats = PivotChart(
        datasource = dateRevenue,
        series_options =
          [{'options':{
              'type': 'line'},
            'terms':[
              'avg_revenue']
              }],
        chart_options =
          {'title': {
               'text': 'Spend over Last 30 days'}})
					   
	return render(request,'monthly_stats.html',
                    {
                        'transaction_stats': transaction_stats,
                        'store_list' : store_list

                    }
                )	

@csrf_exempt		
def revenue_chart(request):
	store =  Store.objects.all()
	output = []
	for s in store:
		if s.region not in output:
			output.append(s.region)
	print output			
	context = {'country':output}  
	return render (request,'transaction_stats.html',context)	
	
@csrf_exempt	
def revenue_pie(request):
	d =  json.loads(request.body)
	print d['region']
	transaction_list = Transaction.objects.all()
	dict = {}
	for t in transaction_list:
		storeid = t.store_id
		store = Store.objects.get(store_id=storeid)
		if (store.region == d['region']):
			if dict.has_key(storeid):
				value = dict.get(storeid)
				value = value+t.selling_price*t.quantity_sold
				dict[storeid]=value
			else:
				value = t.selling_price*t.quantity_sold
				dict[storeid] = value
	
	for key in dict:
		dict[key] = str(dict.get(key))
	
	payload = {
       'result':dict
	}
	data = json.dumps(payload)
	print data
	return HttpResponse(data,mimetype='application/json')
	 
	 


