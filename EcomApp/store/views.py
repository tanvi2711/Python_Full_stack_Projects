from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib.messages import info,error
from . import models
from . import forms 
# Create your views here.
def storeIndexView(request):
  products=models.ProductModelClass.objects.all()[::-1]
  categories=models.CategoryModelClass.objects.all()
  if 'user_id' in request.session:
    username=request.session.get('name')
    return render(request,"store_index.html",{'products':products,'categories':categories,'username':username})
  else:
    return render(request,"store_index.html",{'products':products,'categories':categories})
 

def storeProductsView(request,category):
  categories=models.CategoryModelClass.objects.all()
  singleCategoryObj=models.CategoryModelClass.objects.get(name=category)
  products=models.ProductModelClass.objects.filter(category=singleCategoryObj.id)
  print(products)
  if 'user_id' in request.session:
    username=request.session.get('name')
    return render(request,"store_index.html",{'products':products,'categories':categories,'username':username})
  else:
    return render(request,"store_index.html",{'products':products,'categories':categories})
 
  return render(request,"products.html",{'categories':categories,'category':category,'products':products})

def storeLoginView(request):
  if request.method=="POST":
    mobile=request.POST.get("mobile")
    password=request.POST.get("password")
    user=models.UserModelClass.objects.filter(mobile=mobile,password=password)
    if user.count()>0:
      user=user[0]
      request.session['name']=user.name
      request.session['user_id']=user.id
      return redirect("storeIndex")
    else:
      info(request,"Invalid Login Credentials ❌")
  return render(request,"storelogin.html")

def storeLogoutView(request):
  request.session.flush()
  return redirect("storeIndex")

def storeCreateAccountView(request):
  if request.method=="POST":
    form=forms.UserModelForm(request.POST)
    if form.is_valid():
      form.save()
      info(request,"Account Created Successfully ✅")
      return redirect("storelogin")
    else:
      error(request,"Error in Creating Account")
  form=forms.UserModelForm()
  return render(request,"storecreateaccount.html",{'form':form})
def addcartView(request,product_id):
  product=models.ProductModelClass.objects.get(id=product_id)
  if 'user_id' in request.session:
    user_id=request.session.get('user_id')
    user=models.UserModelClass.objects.get(id=request.session['user_id'])
    models.cartModelClass.objects.create(user=user,product=product)
    info(request,"Product Added to Cart Successfully")
    return redirect("storeproductscategory",product.category.name)
  else:
    info(request,"Please Login to Add Products to Cart")
    return redirect(f"storeproductscategory/{product.category.name}")

def displayCartView(request):
  if 'user_id' in request.session:
    username=request.session.get('name')
    categories=models.CategoryModelClass.objects.all()
    user_id=request.session.get('user_id')
    user=models.UserModelClass.objects.get(id=request.session['user_id'])
    cartitems=models.cartModelClass.objects.filter(user=user)
    return render(request,"displaycart.html",{'cartitems':cartitems,'categories':categories,'username':username})
  return redirect(request,"displaycart.html",{'categories':categories})

def deleteCartView(request,cart_id):
  cartitem=models.cartModelClass.objects.get(id=cart_id).delete()
  info(request,"Cart Item Deleted Successfully")
  return redirect("displaycart")
def billCartView(request):
  if 'user_id' in request.session:
    username=request.session.get('name')
    categories=models.CategoryModelClass.objects.all()
    user_id=request.session.get('user_id')
    user=models.UserModelClass.objects.get(id=request.session['user_id'])
    cartitems=models.cartModelClass.objects.filter(user=user)
    total=0
    for item in cartitems:
      total+=item.product.price
    GST=total*0.12
    deliverycharges=50
    finaltotal=total+GST+deliverycharges
    return render(request,"billcart.html",{'cartitems':cartitems,'total':total,'GST':GST,'deliverycharges':deliverycharges,'finaltotal':finaltotal})

def orderCartView(request):
  if 'user_id' in request.session:
    username=request.session.get('name')
    categories=models.CategoryModelClass.objects.all()
    user_id=request.session.get('user_id')
    user=models.UserModelClass.objects.get(id=request.session['user_id'])
    cartitems=models.cartModelClass.objects.filter(user=user)
    paymethod=request.POST.get("paymethod")
    address=request.POST.get("address")
    for item in cartitems:
      product=item.product
      finalprice=product.price+(product.price*0.12)+50
      models.OrderModelClass.objects.create(
        user=user,
        product=product,
        finalprice=finalprice,
        paymentmethod=paymethod,
        address=address,
        orderstatus="Order Placed"
      )
      item.delete()
    info(request,"Order Placed Successfully")
  return render(request,"ordersuccess.html")

def orderHistoryView(request):
  if 'user_id' in request.session:
    username=request.session.get('name')
    categories=models.CategoryModelClass.objects.all()
    user_id=request.session.get('user_id')
    user=models.UserModelClass.objects.get(id=request.session['user_id'])
    orders=models.OrderModelClass.objects.filter(user=user).order_by('-id')
    return render(request,"orderhistory.html",{'orders':orders,'categories':categories,'username':username})
  return redirect("storeIndex")

def cancelOrderView(request,order_id):
  order=models.OrderModelClass.objects.filter(id=order_id).update(orderstatus="Order Cancelled")
  return redirect("orderhistory")

# def storeSearchView(request):
#   return render(request,"search.html")
from django.db.models import Q

def storeSearchView(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = models.ProductModelClass.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(request, "search.html", {
        "query": query,
        "results": results
    })


def billProductView(request, productid):
    if 'user_id' in request.session:
        user_id = int(request.session.get('user_id'))
        username =request.session.get('name')

        user = models.UserModelClass.objects.get(id=user_id)
        categories = models.CategoryModelClass.objects.all()
        products = models.ProductModelClass.objects.filter(id=productid)

        total = products[0].price
        GST = total * 0.12
        deliverycharges = 50
        finaltotal = total + GST + deliverycharges

        return render(
            request,
            "billproduct.html",
            {
                'products': products,
                'categories': categories,
                'username': username,
                'GST': GST,
                'deliverycharges': deliverycharges,
                'finaltotal': finaltotal,
                'total': total,
                'productsid': productid
            }
        )

    # ❌ NOT LOGGED IN
    else:
      return redirect('storelogin')   # use your login URL name
      messages(request, "Please Login to Continue")
def OrderProductView(request,productid):
  if 'user_id' in request.session:
    user_id=request.session.get('user_id')
    username=request.session.get('name')
    categories=models.CategoryModelClass.objects.all()
    user=models.UserModelClass.objects.get(id=user_id)
    paymethod=request.POST.get("paymethod")
    address=request.POST.get("address")
    products=models.ProductModelClass.objects.filter(id=productid)
    finalprice=products[0].price+(products[0].price*0.12)+50
    models.OrderModelClass.objects.create(product=products[0],user=user,finalprice=finalprice,paymentmethod=paymethod,address=address,orderstatus='order placed') 

    return render(request,"ordersuccess.html")

