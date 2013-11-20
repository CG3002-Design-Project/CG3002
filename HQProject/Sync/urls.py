from django.conf.urls import patterns, url

from Sync import views


urlpatterns = patterns('',
    url(r'^processInventory$', views.localPushInventory, name='localPushInventory'),
    url(r'^processTransactions$', views.localPushTransaction, name='localPushTransaction'),
    url(r'^processRequest$',views.localPushRequests, name = 'localPushRequests'),
    url(r'^processProduct$', views.localPushProduct, name='localPushProduct'),
    url(r'^receiveProduct$', views.localPullProduct, name='localPullProduct'),
    url(r'^receiveInventory$',views.localPullInventory,name='localPullInventory')
   # url(r'^sync_function$', views.sync_function, name='sync_function'),
)

