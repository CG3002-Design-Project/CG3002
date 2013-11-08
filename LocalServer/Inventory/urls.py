from django.conf.urls import patterns, url

from Inventory import views

urlpatterns = patterns('',
    url(r'^calculate_transaction$', views.calculate_transaction, name='calculate_transaction'),
	url(r'^sync_function$', views.sync_function, name='sync_function'),
	url(r'^transaction_sync$', views.transaction_sync, name='transaction_sync'),
	url(r'^sync_function/hq_sync$', views.sync_with_hq, name='sync_with_hq'),
	url(r'^$', views.pull_from_hq, name='pull_from_hq'),
	url(r'^returnPrice$', views.return_price, name='return_price'),
	#url(r'^view-product$', views.view_product, name='view_product'),
	#url(r'^view-product/(\d+)/storewise$', views.view_storewise, name='view_storewise'),
	#url(r'^created$', views.created_store, name='created_store'),
	#url(r'^update-store$', views.update_store, name='update_store'),
	#url(r'^view-stores$', views.view_stores, name='view_stores'),
	#url(r'^updated$', views.updated_store, name='updated_store'),
)