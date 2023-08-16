from django.urls import reverse
from .models import Order, OrderItem, Product,Collection
from django.shortcuts import redirect, render,get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm, SearchForm

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

def product_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.available.filter(title__icontains = query)
            # results = Product.available.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,'store/product/search.html', {'form': form,'query': query,'results': results})

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


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],quantity=item['quantity'])
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,'store/order/create.html',{'cart': cart, 'form': form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'store/order/detail.html',{'order': order})