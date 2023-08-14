from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('', views.product_list, name='product_list'),
    path('<slug:collection_slug>/', views.product_list,name='product_list_by_collection'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/<int:product_id>/',views.cart_remove, name='cart_remove'),
]
