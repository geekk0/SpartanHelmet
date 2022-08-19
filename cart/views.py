from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Categories, Items
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Items, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Items, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    session_info = request.session.items()
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_plus_one(request, product_id, quantity):
    cart = Cart(request)
    product = get_object_or_404(Items, id=product_id)
    cart.plus_one(product, quantity)
    return redirect('cart_detail')


def cart_minus_one(request, product_id, quantity):
    cart = Cart(request)
    product = get_object_or_404(Items, id=product_id)
    cart.minus_one(product, quantity)
    return redirect('cart_detail')

