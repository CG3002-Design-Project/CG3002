from django.conf.urls.defaults import *

from userprofile import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)

