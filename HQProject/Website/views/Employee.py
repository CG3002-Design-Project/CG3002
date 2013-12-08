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
from Website.models import Store,Product,Inventory,Transaction
from decimal import *
import random    
     
@login_required
def view_employee(request):
    employee_list = Employee.objects.filter(designation="Store Manager")    
    context = {'employee_list': employee_list}   
    return render(request, 'view_employee.html',context)

@login_required
def send_sms(request,id):
    context = {}
    return render(request, 'send_sms.html',context)