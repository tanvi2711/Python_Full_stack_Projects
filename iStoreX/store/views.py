from django.shortcuts import render,redirect
from . import models
from .models import *
from django.contrib.auth import authenticate, login

# Create your views here.

def storeIndexView(request):
    categories=CategoryModelClass.objects.all()
    products=ProductModelClass.objects.all()
    return render(request,"index.html",{'categories':categories,'products':products})

def storeProductView(request,category):
    categories=CategoryModelClass.objects.all()
    category_obj=CategoryModelClass.objects.get(name=category)
    products=ProductModelClass.objects.filter(category=category_obj.id)
    return render(request,"products.html",{'products':products,'categories':categories,'category_name':category_obj.name})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
