from django.conf.urls import patterns, url
from Customer import views

urlpatterns = patterns('',
    url(r'^customer_home/$', views.customer_home, name='customer_home'),
	url(r'^inventory_list/$', views.inventory_list, name='inventory_list'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^cart/order_placed/$', views.order_placed, name='order_placed'),
#    url(r'^fb_login/$', views.fb_login, name='fb_login'),
#    url(r'^facebook/$', 'views.facebook', name='facebook'),
#    url(r'^accounts/', include('allauth.urls')))
)
