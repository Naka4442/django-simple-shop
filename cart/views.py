from django.shortcuts import render, redirect
from products.models import Product

def cart_add(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'total': product.price * cart[str(product.id)]
        })
    return render(request, 'cart/view.html', {'cart_items': cart_items})