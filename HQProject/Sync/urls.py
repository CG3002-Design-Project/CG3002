from django.conf.urls import patterns, url

from Sync import views


urlpatterns = patterns('',
    url(r'^processInventory$', views.process, name='process'),
    url(r'^processTransactions$', views.processT, name='processT'),
)
