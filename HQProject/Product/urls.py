from django.conf.urls import patterns, url

from Product import views

urlpatterns = patterns('',
    url(r'^$', views.filter_products, name='filter_products'),
	
	url(r'^view-product$', views.view_product, name='view_product'),
	url(r'^view-product/(\d+)/storewise$', views.view_storewise, name='view_storewise'),
	#url(r'^created$', views.created_store, name='created_store'),
	#url(r'^update-store$', views.update_store, name='update_store'),
	#url(r'^view-stores$', views.view_stores, name='view_stores'),
	#url(r'^updated$', views.updated_store, name='updated_store'),
)