from django.urls import *
from . import views

urlpatterns = [
    path('',views.storeIndexView,name='storeIndex'),
    path('products/<category>',views.storeProductsView,name='storeproductscategory'),
]
