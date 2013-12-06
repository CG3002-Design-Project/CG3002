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
from decimal import *
import random
import json
from datetime import date

@login_required
def transaction_home(request):
	transaction_list = Transaction.objects.all()
	context = {'transaction_list':transaction_list}
	return render(request, 'transaction_home.html',context)

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
	 
	 

@login_required
def transaction_stats(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    if 'store_selected' in request.GET and request.GET['store_selected']:
      store_selected = request.GET['store_selected']
    else:
      store_selected = "All"
    startdate = date.today()
    
    if (store_selected=="All"):
      transaction_list_thirty= Transaction.objects.all()
      transaction_list_annual= Transaction.objects.all()
    else:
      transaction_list_thirty= Transaction.objects.filter(store_id=store_selected)
      transaction_list_annual= Transaction.objects.filter(store_id=store_selected)

    store_list = Store.objects.all()

    storeRevenueOld = \
        DataPool(
           series=
            [{'options': {
               'source': Transaction.objects.all()},
              'terms': [
                'store_id',
                'transaction_date',
                'cost_price']}
             ])

    storeRevenue = \
        PivotDataPool(
          series=
            [{'options': {
               'source': Transaction.objects.all(),
               'categories' : ['store_id']},
              'terms': {
                'total_revenue': Sum('selling_price')}}])

    def store_name(total_revenue):
        #store_map = {123456: 'Store1', 781234: 'Store2'}
        #return store_map[store_id]
        return total_revenue

    def datename(transaction_date):
        return transaction_date

    def product_findname(product_id):
        product_list=Product.objects.get(product_id=product_id)
        return  product_list.name

    def monthname(month_num):
        names ={1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        return names[month_num]
#    transactions_last12= Transaction.objects.filter(transaction_date.year>2010)
    dateRevenue = \
        PivotDataPool(
          series=
            [{'options': {
               'source': transaction_list_thirty,
               'categories' : ['transaction_date']},
              'terms': {
                'avg_revenue_thirty': Avg('cost_price')}},
             {'options': {
               'source': transaction_list_annual,
               'categories' : ['transaction_date']},
              'terms': {
                'avg_revenue_annual': Avg('cost_price')}}
                ])
                #'top_n' : 10}}])


    transaction_stats0 = PivotChart(
        datasource = storeRevenue,
        series_options =
          [{'options':{
              'type': 'pie'},
            'terms':[
              'total_revenue']
              }],
        chart_options =
          {'title': {
               'text': 'Spend per Store'}})
        #x_sortf_mapf_mts = (None, store_name, False))

    transaction_stats1 = PivotChart(
        datasource = dateRevenue,
        series_options =
          [{'options':{
              'type': 'line'},
            'terms':[
              'avg_revenue_thirty']
              },
           {'options':{
              'type': 'pie',
              'center': [150, 100],
              'size': '50%'},
            'terms':[
              'avg_revenue_annual']
              }],
        chart_options =
          {'title': {
               'text': 'Spend over Last 30 days (line) and Spend over Year by Month'}})

#        x_sortf_mapf_mts = [(None, None, False), (None, monthname, False)])
#        x_sortf_mapf_mts = [(None, datename, False),(None, storename, False)])

    productrevenue = \
        PivotDataPool(
          series=
            [{'options': {
               'source': transaction_list_annual,
               'categories' : ['product_id']},
              'terms': {
                'avg_revenue': Avg('cost_price')}}],
                #'top_n' : 10}}]
          top_n = 10,
          top_n_term = 'avg_revenue')

    transaction_stats2 = \
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

    return render(request,'transaction_stats.html',
                    {
#                        'transaction_stats': [transaction_stats1, transaction_stats2],
#                        'store_list' : store_list
                        'transaction_stats': [transaction_stats0, transaction_stats1, transaction_stats2],
                        'store_list' : store_list
                    }
                )

