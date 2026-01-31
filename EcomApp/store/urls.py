from django.urls import path
from . import views
urlpatterns = [
  path("",views.storeIndexView,name="storeIndex"),
  path("products/<category>",views.storeProductsView,name="storeproductscategory"),
  path("login",views.storeLoginView,name="storelogin"),
  path("createaccount",views.storeCreateAccountView,name="storeCreateAccount"),
  path("logout",views.storeLogoutView,name="storelogout"),
  path("addcart/<int:product_id>",views.addcartView,name="addcart"),
  path("displaycart",views.displayCartView,name="displaycart"),
  path("deletecart/<int:cart_id>",views.deleteCartView,name="deletecart"),
  path("billcart",views.billCartView,name="billcart"),
  path("ordercart",views.orderCartView,name="ordercart"),
  path("orderhistory",views.orderHistoryView,name="orderhistory"),
  path("search",views.storeSearchView,name="storesearch"),
  path("cancelorder/<int:order_id>",views.cancelOrderView,name="cancelorder"),
  path("billproduct/<productid>",views.billProductView,name="billproduct"),
  path("orderproduct/<productid>",views.OrderProductView,name="Orderproduct"),
  
  
  ]