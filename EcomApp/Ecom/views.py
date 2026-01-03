from django.shortcuts import render
from django.contrib.messages import *
from . import models
from . import forms


# Create your views here.
def index(request):
    categories =models.Category.objects.all()
    products =models.Product.objects.all()
    return render(request,'index.html',{'categories':categories, 'products':products})

def products(request,category):
	categories=models.Category.objects.all()
	category_obj=models.Category.objects.get(name=category)
    products=models.Product.objects.filter(category=category_obj)
    return render(request,'products.html',{'categories':categories,'products':products})

