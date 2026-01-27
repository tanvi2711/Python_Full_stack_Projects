from django.urls import *
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.storeIndexView,name='storeIndex'),
    path('products/<category>',views.storeProductView,name='products'),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/",auth_views.LogoutView.as_view(next_page="storeIndex"),
    name="logout"),
    path("cart/", views.cart_view, name="cart"),
    path("addcart/<int:product_id>/", views.addcart_view, name="addcart"),
    path("removefromcart/<int:cart_item_id>/", views.removefromcart_view, name="removefromcart"),
    path('billing/', views.billing_view, name='billing'),
    path("fake-payment/", views.fake_payment_view, name="fake_payment"),
    path("payment-success/", views.payment_success_view, name="payment_success"),
    path("buy-now/<int:product_id>/", views.buy_now_view, name="buy_now"),
    path("collections/", views.collections_view, name="collections"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)