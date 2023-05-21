import json
from .models import Product,Cart, CartItem, ProductImage
from django.shortcuts import render,get_object_or_404,get_list_or_404

def product_list(request):
    products = Product.objects.all()
    context = {"products": products[:12]}
    return render(request,"store/products.html",context)


def get_or_create_cart(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        try:
            cart = Cart.objects.get(pk=cart_id)
        except:
            cart = Cart.objects.create()
            cart.save()
        finally:
            cart_id = cart.id
        request.session['cart_id'] =str(cart_id)
    return cart_id
    

def add_cart_item(request,pk):
    cart_id = get_or_create_cart(request)
    # product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, pk=pk)
    quantity = request.POST.get('quantity',1)
    item = CartItem.objects.create(cart_id=cart_id,product_id=product.id,quantity=quantity)
    item.save()
    return render(request,"store/cart.html")

def cart_item_list(request):
    cart_id = get_or_create_cart(request)
    cartItems = CartItem.objects.filter(cart=cart_id)
    context={"items":cartItems}
    return render(request,"store/cart.html",context)

