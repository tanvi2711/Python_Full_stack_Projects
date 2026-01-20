from django.urls import *
from . import views

urlpatterns = [
    path('',views.storeIndexView,name='storeIndex'),
    path('products/<category>',views.storeProductView,name='products'),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
]