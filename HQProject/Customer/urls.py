from django.conf.urls import patterns, url

from Customer import views

urlpatterns = patterns('',
    url(r'^customer_home/$', views.customer_home, name='customer_home'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^cart/order_placed/$', views.order_placed, name='order_placed'),
)

