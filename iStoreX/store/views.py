from django.shortcuts import render,redirect
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

def storeIndexView(request):
    categories=CategoryModelClass.objects.all()
    products=ProductModelClass.objects.all()
    return render(request,"index.html",{'categories':categories,'products':products})

@login_required
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

            # ✅ redirect to next page if exists
            next_url = request.GET.get("next")
            return redirect(next_url or "storeIndex")

        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


def signup_view(request):
    return render(request, "signup.html")

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

@login_required
def profile_view(request):
    return render(request, "profile.html")

@login_required
def addcart_view(request, product_id):
    if request.method == "POST":
        product = ProductModelClass.objects.get(id=product_id)
        user = request.user

        # prevent duplicate cart items
        cart_item, created = CartModelClass.objects.get_or_create(
            user=user,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

    return redirect("cart")

@login_required
def cart_view(request):
    user = request.user
    cart_items = CartModelClass.objects.filter(user=user)

    return render(request, "cart.html", {
        "cart_items": cart_items
    })

@login_required
def removefromcart_view(request, cart_item_id):
    cart_item = CartModelClass.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect("cart")



@login_required
def billing_view(request):
    pass