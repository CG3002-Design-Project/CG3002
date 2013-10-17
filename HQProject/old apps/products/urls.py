from django.conf.urls.defaults import *
from HQProject.products import views

urlpatterns = patterns('',
    # ...
    url(r'^search-form/$', views.search_form),
    url(r'^search/$',views.search),
    # ...
)
