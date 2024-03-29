from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('search/', views.product_search, name='product_search'),
    path('order/<int:order_id>/', views.admin_order_detail,name='admin_order_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('', views.product_list, name='product_list'),
    path('<slug:collection_slug>/', views.product_list,name='product_list_by_collection'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/<int:product_id>/',views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
]
