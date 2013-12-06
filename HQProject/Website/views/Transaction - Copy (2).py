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
from django.db.models import Avg, Sum
from Website.models import Store,Product,Inventory,Transaction
from decimal import *
from chartit import DataPool, PivotDataPool, Chart, PivotChart
import random
import simplejson

@login_required
def transaction_home(request):
    transaction_list = Transaction.objects.all()
    context = {'transaction_list':transaction_list}
    return render(request, 'transaction_home.html',context)

@login_required
def transaction_stats(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    if 'store_selected' in request.GET and request.GET['store_selected']:
      store_selected = request.GET['store_selected']
    else:
      store_selected = "All"

    if (store_selected=="All"):
      transaction_list= Transaction.objects.all()
    else:
      transaction_list= Transaction.objects.filter(store_id=store_selected)

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
                'total_revenue': Sum('cost_price')}}])

    def store_name(store_id):
        return store_id

    def datename(transaction_date):
        return transaction_date

    def product_findname(product_id):
        product_list=Product.objects.get(product_id=product_id)
        return  product_list.name

#    transactions_last12= Transaction.objects.filter(transaction_date.year>2010)
    dateRevenue = \
        PivotDataPool(
          series=
            [{'options': {
               'source': transaction_list,
               'categories' : ['transaction_date']},
              'terms': {
                'avg_revenue': Avg('cost_price')}}])
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
#        x_sortf_mapf_mts = (None, store_name, False))

    transaction_stats1 = PivotChart(
        datasource = dateRevenue,
        series_options =
          [{'options':{
              'type': 'line'},
            'terms':[
              'avg_revenue']
              }],
        chart_options =
          {'title': {
               'text': 'Spend over Last 30 days (line)'}})
#        x_sortf_mapf_mts = [(None, datename, False),(None, storename, False)])

    productrevenue = \
        PivotDataPool(
          series=
            [{'options': {
               'source': transaction_list,
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

