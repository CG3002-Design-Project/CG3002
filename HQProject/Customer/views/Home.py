from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction
from decimal import *
import random
import httplib2
import urllib
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import simplejson as json
from Customer.models import Profile

def customer_home(request): 
    return render(request, 'customer_home.html')

def fb_login(request):
    context = {}
    return render(request,'fb_login.html', context)

from django.db import models
from django.contrib.auth.models import User

class FacebookSessionError(Exception):   
    def __init__(self, error_type, message):
        self.message = message
        self.type = error_type
    def get_message(self): 
        return self.message
    def get_type(self):
        return self.type
    def __unicode__(self):
        return u'%s: "%s"' % (self.type, self.message)
        
class FacebookSession(models.Model):

    access_token = models.CharField(max_length=103, unique=True)
    expires = models.IntegerField(null=True)
        
    user = models.ForeignKey(User, null=True)
    uid = models.BigIntegerField(unique=True, null=True)
        
    class Meta:
        unique_together = (('user', 'uid'), ('access_token', 'expires'))
        
    def query(self, object_id, connection_type=None, metadata=False):
        import urllib
        import simplejson
        
        url = 'https://graph.facebook.com/%s' % (object_id)
        if connection_type:
            url += '/%s' % (connection_type)
        
        params = {'access_token': self.access_token}
        if metadata:
            params['metadata'] = 1
         
        url += '?' + urllib.urlencode(params)
        response = simplejson.load(urllib.urlopen(url))
        if 'error' in response:
            error = response['error']
            raise FacebookSessionError(error['type'], error['message'])
        return response
