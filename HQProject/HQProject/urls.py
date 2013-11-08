from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HQProject.views.home', name='home'),
    # url(r'^HQProject/', include('HQProject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	#(r'^statinfo/$', 'homepage.views.stat_info'),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/accounts/login'}),
    #(r'^mainmenu/$', 'homepage.views.mainmenu'),
	#(r'^search-form/$','products.views.search_form'),
    #(r'^search/$','products.views.search')
	url(r'^Store/', include('Store.urls')),
	url(r'^Product/', include('Product.urls')),
        url(r'^Sync/',include('Sync.urls')),      
    	url(r'^Transactions/', include('Transactions.urls')),
    	url(r'^statinfo/$', 'login.views.stat_info'),
    	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/accounts/login'}),
    	url(r'^home/$', 'login.views.home'))