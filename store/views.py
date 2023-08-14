from .models import Product,Cart,Collection
from django.shortcuts import redirect, render,get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm

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
    cart_product_form = CartAddProductForm()
    return render(request,"store/product/detail.html",{"product":product,'cart_product_form': cart_product_form})

@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product,cd["quantity"],cd["override"])
    
    return redirect('store:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('store:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    print("cart len:",len(cart))
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'override': True})
    return render(request, 'store/cart/detail.html', {'cart': cart})
