from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:collection_slug>/', views.product_list,name='product_list_by_collection'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
