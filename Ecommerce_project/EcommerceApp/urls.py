
from django.urls import path
from .import views
app_name = 'EcommerceApp'
urlpatterns = [
    path('Templates_common', views.Templates_common),
    path('', views.Index, name="Index"),
    path('Register', views.Register, name="Register"),
    path('Login', views.Login, name="Login"),
    path('product_details/<slug:slug>/', views.Product_details_view.as_view(), name="product_details"),
    path('add_cart/<pk>', views.add_to_cart, name="add_cart"),
    path('cart_view', views.cart_view, name="cart_view"),
    path('remove_item_from_cart/<pk>', views.remove_item_from_cart, name="remove_item_from_cart"),
    path('incresae_cart/<pk>', views.incresae_cart, name="incresae_cart"),
    path('decrease_cart/<pk>', views.decrease_cart, name="decrease_cart"),
    path('athur_reg', views.athur_reg, name="athur_reg"),
]
