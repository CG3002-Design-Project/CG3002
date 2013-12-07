from Transaction import *
from Inventory import *
from Restock import *
from Store import *
from Sync import *
from Product import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from django.db.models import Avg, Sum
from Website.models import Store,Product,Inventory,Transaction, Employee
from decimal import *
import random
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required 
@login_required
def profile(request):
    curr_employee=Employee.objects.get(user_id=request.user.id)
    context = {'curr_employee':curr_employee}
    return render(request, 'profile.html',context)
 
@staff_member_required   
@login_required
def edit_profile(request,id):
    curr_employee=Employee.objects.get(user_id=request.user.id)
    context = {'curr_employee':curr_employee}
    return render(request,'edit_profile.html',context)
      
@staff_member_required
@login_required
def profile_edited(request,id):
    print id
    curr_employee=Employee.objects.get(user_id=request.user.id)
    address = request.GET['address']
    phone = phone.GET['phone']
    curr_employee.address = address
    curr_employee.phone = phone
    curr_employee.save()
    curr_employee=Employee.objects.get(user_id=request.user.id)
    message = 'Your details have been updated!'
    context = {'curr_employee':curr_employee,'message':message}
    return render(request,'profile.html',context) 