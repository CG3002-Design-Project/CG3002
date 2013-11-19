from django.conf.urls import patterns, url

from Website import views

urlpatterns = patterns('',
    url(r'^filter-products$', views.filter_products, name='filter_products'),
	url(r'^view-product$', views.view_product, name='view_product'),
	url(r'^add-product$', views.add_product, name='add_product'),
	url(r'^add-product/product-added$', views.product_added, name='product_added'),
	url(r'^view-product/(\d+)/storewise$', views.view_storewise, name='view_storewise'),
    url(r'^view-stores$', views.view_stores,name='view_stores'),
    url(r'^filter-stores$', views.filter_stores,name='filter_stores'),
    url(r'^view-stores/create-store$',views.create_store,name='create_store'),
    url(r'^view-stores/(\d+)/edit-store$',views.edit_store,name='edit_store'),
	url(r'^view-stores/(\d+)/store-edited$',views.store_edited,name='store_edited'),
    url(r'^view-stores/create-store/store-created$',views.store_created,name='store_created'),
	url(r'^view-stores/(\d+)/store-deleted$',views.store_deleted,name='store_deleted'),
    url(r'^view/(\d+)/$', views.view_specific,name='view_specific'),
    url(r'^view/(\d+)/inventory-control/create-product$', views.create_product,name='create_product'),
    url(r'^view/inventory-control/(\d+)/product-created$', views.product_created,name='product_created'),
	url(r'^view/inventory-control/(\d+)/search$', views.search,name='search'),
    url(r'^view/(\d+)/inventory-control$', views.inventory_control,name='inventory_control'),
    url(r'^view/inventory-control/(\d+)/(\d+)/edit-product$', views.edit_product,name='edit_product'),
	url(r'^view/inventory-control/(\d+)/add-inventory$', views.add_inventory,name='add_inventory'),
	url(r'^view/inventory-control/(\d+)/inventory-added$', views.inventory_added,name='inventory_added'),
	url(r'^view/inventory-control/(\d+)/(\d+)/product-edited$', views.product_edited,name='product_edited'),
    url(r'^view/inventory-control/(\d+)/(\d+)/(\d+)/edit-inventory$', views.edit_inventory,name='edit_inventory'),
    url(r'^view/inventory-control/(\d+)/(\d+)/(\d+)/inventory-updated$', views.inventory_updated,name='inventory_updated'),
    url(r'^view/inventory-control/(\d+)/(\d+)/(\d+)/inventory-deleted$', views.inventory_deleted,name='inventory_deleted')
)