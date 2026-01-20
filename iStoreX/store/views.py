from django.shortcuts import render , redirect
from django.contrib.messages import info,error
from . import forms
from . import models
from .models import *

# Create your views here.

def storeIndexView(request):
    categories=CategoryModelClass.objects.all()
    produts=ProductModelClass.objects.all()[0:1]
    return render(request,"index.html",{'categories':categories})

def storeProductsView(request,category):
    categories=CategoryModelClass.objects.all()
    category_obj=CategoryModelClass.objects.get(name=category)
    product=ProductModelClass.objects.filter(category=category_obj.id)
    return render(request,'products.html',{'product':product,'categories':categories})