from django.conf.urls import patterns, url

from Inventory import views

urlpatterns = patterns('',
    url(r'^transaction$', views.calculate_transaction, name='transaction'),
	url(r'^display$', views.price_display, name='display'),
	url(r'^sync$', views.sync_function, name='sync'),
	url(r'^product$', views.product_list, name='product'),
	url(r'^product/(\d+)/edit_product$', views.edit_product, name='edit_product'),
	url(r'^product/update_product$', views.update_product, name='update_product'),
	url(r'^inventory$', views.inventory_list, name='inventory'),
	url(r'^inventory/update_inventory$', views.update_inventory, name='update_inventory'),
	url(r'^inventory/(\d+)/(\d+)/edit_inventory$', views.edit_inventory, name='edit_inventory'),
	url(r'^returnPrice$', views.return_price, name='return_price'),
	url(r'^saveTransaction$', views.save_transaction, name='save_transaction'),
	url(r'^restock$',views.restock_qty,name='restock_qty'),	
	url(r'^addQuantity$', views.add_qty_back, name='add_qty_back'),	
	url(r'^check_display$', views.check_display, name='check_display'),	
	url(r'^setDisplayID$', views.setDisplayID, name='setDisplayID'),
	url(r'^sync/transaction_sync$', views.transaction_sync, name='transaction_sync'),
	url(r'^sync/inventory_sync$', views.inventory_sync, name='inventory_sync'),
	url(r'^sync/request_details_sync$', views.request_details_sync, name='request_details_sync'),
	url(r'^sync/product_sync$', views.product_sync, name='product_sync'),
	url(r'^sync/pull_product_from_hq$', views.pull_product_from_hq, name='pull_product_from_hq'),
	url(r'^sync/pull_inventory_from_hq$', views.pull_inventory_from_hq, name='pull_inventory_from_hq'),
	url(r'^sync/update_perishable_price$', views.update_perishable_price, name='update_perishable_price'),
	url(r'^sync/update_nonperishable_price$', views.update_nonperishable_price, name='update_nonperishable_price'),
)