
from django.views.generic import ListView
from .models import Product,Cart

class ProductList(ListView):
    model = Product
    template_name = "store/products.html"
    context_object_name="products"
    paginate_by=12

class CartList(ListView):
    model = Cart
    template_name = "store/cart.html"
    context_object_name="cart"
    paginate_by=12