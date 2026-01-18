from django.shortcuts import render
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib.messages import info,error
from django.contrib.auth.decorators import login_required
from . import models
from . import forms 
# Create your views here.
# Create your views here.
def index(request):
    return render(request,"index.html")

@login_required(login_url='/accounts/login/')
def career(request):
    user = request.user
    print(user.email)
    print(user.get_full_name())
    return render(request,"career.html",{"user":user})

