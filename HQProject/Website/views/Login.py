from Transaction import *
from Inventory import *
from Restock import *
from Store import *
from Sync import *
from Product import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import Context, loader, RequestContext
from Website.models import Store,Product,Inventory,Transaction, Employee
from django.contrib.auth.models import User
#https://docs.djangoproject.com/en/1.2/topics/auth/#other-authentication-sources
#http://stackoverflow.com/questions/9825630/login-required-decorator-in-django-1-1-and-template-name

#@login_required(redirect_field_name='my_redirect_field')
#@login_required
#def garbage_stat_info(request):
#    template = loader.get_template('stat_info.html')
#    context = Context({'is_auth': str(request.user.is_authenticated())})
#   return HttpResponse(template.render(context))

#@login_required
#ef stat_info(request):
#    return render_to_response('stat_info.html',
#        {'is_auth':request.user.is_authenticated()},
#        context_instance=RequestContext(request))

@login_required
def home(request):
    return render_to_response('home.html',{}, context_instance=RequestContext(request))

@login_required
def home_regionalManager(request):
    return render_to_response('home_regionalManager.html',{}, context_instance=RequestContext(request))

@login_required
def home_storeManager(request):
    curr_employee=Employee.objects.get(user_id=request.user.id)
    context = {'curr_employee':curr_employee}
    return render(request,'home_storeManager.html',context)

@login_required
def login_redirect(request):
    #if request.user.groups.filter(name="Regional Manager"):
    if request.user.is_staff:
        # user is regional manager
        return redirect("/Website/home_regionalManager")
    else:
        return redirect("/Website/home_storeManager")