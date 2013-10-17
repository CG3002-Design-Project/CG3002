from django.conf.urls import patterns, url

from Store import views

urlpatterns = patterns('',
    url(r'^$', views.store_mainpage, name='store_mainpage'),
	url(r'^create-store$', views.create_store, name='create_store'),
	url(r'^created$', views.created_store, name='created_store'),
	url(r'^update-store$', views.update_store, name='update_store'),
	url(r'^view-stores$', views.view_stores, name='view_stores'),
	url(r'^updated$', views.updated_store, name='updated_store'),
)