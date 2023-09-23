from django.shortcuts import render, redirect, get_object_or_404
from shopping_app.models import Product
from .models import Cart,Cartitem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def _cartid(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def addcart(request,product_id):
    product=Product.objects.get(id=product_id)

    try:
        cart=Cart.objects.get(cart_id=_cartid(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cartid(request))
        cart.save(),
    try:
        cart_item=Cartitem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity +=1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item=Cartitem.objects.create(
            product=product,
            quantity=1,
            cart=cart)
        cart_item.save()
    return redirect('cartapp:cart_details')

def cart_details(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cartid(request))
        cart_items=Cartitem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))

def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cartid(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cartitem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartapp:cart_details')

def full_remove(request,product_id):
    cart = Cart.objects.get(cart_id=_cartid(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cartitem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cartapp:cart_details')
