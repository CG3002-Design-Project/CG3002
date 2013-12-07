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
from django.shortcuts import render_to_response
from django.template import RequestContext
#from fbproject.settings import FB_APP_ID, FB_APP_SECRET
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
@login_required
def home(request):
    return render_to_response('home.html',{}, context_instance=RequestContext(request))

@staff_member_required
@login_required
def home_regionalManager(request):
    return render_to_response('home_regionalManager.html',{}, context_instance=RequestContext(request))

@staff_member_required
@login_required
def home_storeManager(request):
    curr_employee=Employee.objects.get(user_id=request.user.id)
    context = {'curr_employee':curr_employee}
    return render(request,'home_storeManager.html',context)

@login_required
def home_accessDenied(request):
    context = {}
    return render(request,'home_accessDenied.html',context)

@login_required
def login_redirect(request):
    #if request.user.groups.filter(name="Regional Manager"):
    if request.user.is_superuser:
        # user is regional manager
        return redirect("/Website/home_regionalManager")
    elif request.user.is_staff:
        return redirect("/Website/home_storeManager")
    else:
        return redirect("/Customer/customer_home")


@login_required
def login_url(request):
    #if request.user.groups.filter(name="Regional Manager"):
    if request.user.is_superuser:
        # user is regional manager
        return redirect("/Website/accounts/login")
    elif request.user.is_staff:
        return redirect("/Website/accounts/login")
    else:
        return redirect("/Customer/accounts/login")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })