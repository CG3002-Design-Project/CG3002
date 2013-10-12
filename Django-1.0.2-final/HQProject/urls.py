from django.conf.urls.defaults import *

#from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^testproject/', include('testproject.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    #(r'^homepage/', include('homepage.urls')),
    (r'^userprofile/', include('userprofile.urls')),
    #(r'^admin/', include(admin.site.urls)),
    (r'^statinfo/$', 'homepage.views.stat_info'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/accounts/login'}),
    (r'^mainmenu/$', 'homepage.views.mainmenu'),
    (r'^search-form/$','products.views.search_form'),
    (r'^search/$','products.views.search')

)


