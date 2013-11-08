from django.conf.urls import patterns, url
from Transactions import views

urlpatterns = patterns('',
    url(r'^$', views.transactions_home, name='transactions_home'),
    #url(r'^add_transaction', views.add_transaction, name='add_transaction'),
    #url(r'^transactions_added', views.transactions_added, name='transactions_added'),
    url(r'^add_transaction$',views.add_transaction,name='add_transaction'),
    url(r'^transactions_added$',views.transactions_added,name='transactions_added'),
	url(r'^(\d+)/(\d+)/edit_transactions$',views.edit_transactions,name='edit_transactions'),
    url(r'^(\d+)/(\d+)/transactions_edited$',views.transactions_edited,name='transactions_edited'),
	#url(r'^(\d+)/(\d+)/delete_transactions$',views.delete_transactions,name='delete_transactions'),
    url(r'^(\d+)/(\d+)/transactions_deleted$',views.transactions_deleted,name='transactions_deleted')
)	
