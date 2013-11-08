from django.conf.urls import patterns, url

from Store import views


urlpatterns = patterns('',
    #url(r'^$', views.store_mainpage, name='store_mainpage'),
	
	#url(r'^create-store$', views.create_store, name='create_store'),
	#url(r'^created$', views.created_store, name='created_store'),
	#url(r'^update-store$', views.update_store, name='update_store'),
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
    url(r'^view/(\d+)/inventory-control$', views.inventory_control,name='inventory_control'),
    url(r'^view/inventory-control/(\d+)/(\d+)/(\d+)/edit-product$', views.edit_product,name='edit_product'),
    url(r'^view/inventory-control/(\d+)/(\d+)/(\d+)/product-updated$', views.product_updated,name='product_updated'),
    url(r'^view/inventory-control/(\d+)/(\d+)/(\d+)/product-deleted$', views.product_deleted,name='product_deleted')
)