import json
from .models import Product,Cart, CartItem, ProductImage,Collection
from django.shortcuts import render,get_object_or_404

def product_list(request,collection_slug=None):
    collection = None
    collections = Collection.objects.all()
    products = Product.available.all()
    if collection_slug:
        collection = get_object_or_404(Collection,slug = collection_slug)
        products = Product.available.filter(collection=collection)
    context = {"products": products[:12],"count":products.count(),"collection": collection,"collections": collections}
    return render(request,"store/product/list.html",context)

def product_detail(request,id,slug):
    product = get_object_or_404(Product, id=id, slug=slug, inventory__gte=1)

    return render(request,"store/product/detail.html",{"product":product})




