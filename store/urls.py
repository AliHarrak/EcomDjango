from django.urls import path
from . import views
from django.contrib.auth import views as login_views
from .views import ProductDetailView

urlpatterns = [
    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),
    path('register/',views.register, name="register"),
    path('login/',views.userLogin, name="login"),
    path('logout/',views.userLogout, name="logout"),
    path('product/<int:pk>',ProductDetailView.as_view(),name="Products_details"), 


]


