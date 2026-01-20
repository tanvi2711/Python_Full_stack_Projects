from django.shortcuts import render,redirect
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import login
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

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("storeIndex")
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })
    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "signup.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        return redirect("storeIndex")

    return render(request, "signup.html")

def forgot_password_view(request):
    return render(request, "forgot_password.html")