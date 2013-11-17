from django.conf.urls import patterns, url

from Sync import views


urlpatterns = patterns('',
    url(r'^processInventory$', views.process, name='process'),
    url(r'^processTransactions$', views.processT, name='processT'),
    url(r'^sync_function$', views.sync_function, name='sync_function'),
)
