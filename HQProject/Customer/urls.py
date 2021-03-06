from django.conf.urls import patterns, url
from Customer import views

urlpatterns = patterns('',
    url(r'^customer_home/$', views.customer_home, name='customer_home'),
	url(r'^inventory_list/(\d+)$', views.inventory_list, name='inventory_list'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^cart/order_placed/$', views.order_placed, name='order_placed'),
	url(r'^add_eTransaction$', views.add_eTransaction, name='add_eTransaction'),
    url(r'^about_us/$', views.about_us, name='about_us'),
	url(r'^render_map/$', views.render_map, name='render_map'),
	url(r'^maps/$', views.maps, name='maps'),
	url(r'^render_storeid$', views.render_storeid, name='render_storeid'),
#    url(r'^fb_login/$', views.fb_login, name='fb_login'),
#    url(r'^facebook/$', 'views.facebook', name='facebook'),
#    url(r'^accounts/', include('allauth.urls')))
)
