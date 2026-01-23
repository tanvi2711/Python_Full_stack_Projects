from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product<category>', views.products, name='products'),

]

