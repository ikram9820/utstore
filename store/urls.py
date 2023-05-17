from django.urls import path

from .views import ProductList,CartList


urlpatterns = [
    path("", ProductList.as_view(), name="products"),  
    path("cart/", CartList.as_view(), name="cart"),  
]