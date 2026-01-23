from django.urls import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.storeIndexView,name='storeIndex'),
    path('products/<category>',views.storeProductView,name='products'),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]