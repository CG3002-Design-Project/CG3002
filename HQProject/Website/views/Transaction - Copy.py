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

def storename(store_id):
    return store_id

def datename(transaction_date):
    return transaction_date

def product_findname(product_id):
    product_list=Product.objects.get(product_id=product_id)
    return  product_list.product_name

@login_required
def transaction_home(request):
    transaction_list = Transaction.objects.all()
    context = {'transaction_list':transaction_list}
    return render(request, 'transaction_home.html',context)
    
@login_required
def transaction_stats(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    #store_selected="All"
    if 'store_selected' in request.GET and request.GET['store_selected']:
      store_selected = request.GET['store_selected']
    else:
      store_selected = "All"

    if (store_selected=="All"):
      transaction_list= Transaction.objects.all()
    else:
      transaction_list= Transaction.objects.filter(store_id=store_selected)

    store_list = Store.objects.all()

    storeRevenue = \
        DataPool(
           series=
            [{'options': {
               'source': Transaction.objects.all()},
              'terms': [
                'store_id',
                'cost_price']}
             ])


    transaction_stats1 = Chart(
        datasource = storeRevenue,
        series_options =
          [
           {'options':{
              'type': 'pie',
              'center': [150, 100],
              'size': '50%'},
            'terms':{
              'store_id': [
                'cost_price']
              }}],
        chart_options = 
          {'title': {
               'text': 'Spend per Date (line) and Revenue per Store (pie)'}},
        x_sortf_mapf_mts = [(None, storename, False)])
   
    productrevenue = \
        PivotDataPool(
          series=
            [{'options': {
               'source': transaction_list,
               'categories' : ['product_id'],
               'top_n_per_cat': 10},
              'terms': {
                'avg_revenue': Avg('cost_price')}}
                #'top_n' : 10}}
             ])

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
                   'text': 'Revenue per Product'},
               'xAxis': {
                    'title': {
                       'text': 'Product ID'}}})

    #return render_to_response('transaction_stats.html',{'transaction_stats': transaction_stats})
    return render(request,'transaction_stats.html',
                    {
                        'transaction_stats': [transaction_stats1, transaction_stats2],
                        'store_list' : store_list
                    }
                )


    # storeRevenue = \
    #     PivotDataPool(
    #        series=
    #         [{'options': {
    #             'source': Transaction.objects.all()
    #           'terms': {
    #             'avg_revenue': Avg('cost_price'),}}
    #          ])

        # storeRevenue = \
        # PivotDataPool(
        #    series=
        #     [{'options': {
        #         'source': Transaction.objects.all(),
        #         'categories' : ['store_id']},
        #       'terms': {
        #         'avg_revenue': Avg('cost_price'),}}
        #      ])


    #Step 2: Create the Chart object
    # transaction_stats1 = Chart(
    #         datasource = storeRevenue,
    #         series_options =
    #           [{'options':{
    #               'type': 'pie',
    #               'stacking': False},
    #             'terms':{
    #               'store_id': [
    #                 'avg_revenue']
    #               }}],
    #         chart_options =
    #           {'title': {
    #                'text': 'Revenue by Stores'}},
    #         x_sortf_mapf_mts = (None,storename,False))