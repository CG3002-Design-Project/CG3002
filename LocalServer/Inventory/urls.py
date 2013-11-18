from django.conf.urls import patterns, url

from Inventory import views

urlpatterns = patterns('',
    url(r'^transaction$', views.calculate_transaction, name='transaction'),
	url(r'^display$', views.price_display, name='display'),
	url(r'^sync$', views.sync_function, name='sync'),
	url(r'^product$', views.product_list, name='product'),
	url(r'^stock$', views.stock_list, name='stock'),
	url(r'^returnPrice$', views.return_price, name='return_price'),
	url(r'^saveTransaction$', views.save_transaction, name='save_transaction'),
	url(r'^restock$',views.restock_qty,name='restock_qty'),	
	url(r'^addQuantity$', views.add_qty_back, name='add_qty_back'),	
	url(r'^display$', views.display, name='display'),	
	url(r'^setDisplayID$', views.setDisplayID, name='setDisplayID'),
	url(r'^sync/transaction_sync$', views.transaction_sync, name='transaction_sync'),
	url(r'^sync/inventory_sync$', views.inventory_sync, name='inventory_sync'),
	url(r'^sync/request_details_sync$', views.request_details_sync, name='request_details_sync'),
	url(r'^sync/product_sync$', views.product_sync, name='product_sync'),
	url(r'^sync/pull_product_from_hq$', views.pull_product_from_hq, name='pull_product_from_hq'),
	url(r'^sync/pull_inventory_from_hq$', views.pull_inventory_from_hq, name='pull_inventory_from_hq'),
	url(r'^sync/update_perishable_price$', views.update_perishable_price, name='update_perishable_price'),
	url(r'^sync/update_nonperishable_price$', views.update_nonperishable_price, name='update_nonperishable_price'),
	#url(r'^$', views.pull_from_hq, name='pull_from_hq')
	#url(r'^view-product$', views.view_product, name='view_product'),
	#url(r'^view-product/(\d+)/storewise$', views.view_storewise, name='view_storewise'),
	#url(r'^created$', views.created_store, name='created_store'),
	#url(r'^update-store$', views.update_store, name='update_store'),
	#url(r'^view-stores$', views.view_stores, name='view_stores'),
	#url(r'^updated$', views.updated_store, name='updated_store'),
)