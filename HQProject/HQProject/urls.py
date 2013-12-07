from django.conf.urls import patterns, include, url
#from social_auth.backends import get_backend

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
    url(r'^admin/', include(admin.site.urls)),
	#(r'^statinfo/$', 'homepage.views.stat_info'),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/accounts/login'}),
    #(r'^mainmenu/$', 'homepage.views.mainmenu'),
	#(r'^search-form/$','products.views.search_form'),
    #(r'^search/$','products.views.search')
	#url(r'^Store/', include('Store.urls')),
	#url(r'^Product/', include('Product.urls')),
	url(r'^Website/', include('Website.urls')),
    url(r'^Customer/', include('Customer.urls')),
    url(r'^Sync/',include('Sync.urls')),
 #   url(r'', include('social_auth.urls')),
)
