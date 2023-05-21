from django.urls import path

from . import views


urlpatterns = [
    path("", views.product_list, name="products"),  
    path("cart/", views.cart_item_list, name="cart"),  
    path("add_item_to_cart/<int:pk>", views.add_cart_item, name="add_to_cart"),  
]