from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from django.views.decorators.http import require_POST
from orders.models import Order, OrderItem  # не забудь импортировать
from orders.forms import CheckoutForm  # твоя форма
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart:cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.warning(request, "Ваша корзина пуста")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = cart.total_price()
            order.save()

            # Создаем OrderItem из CartItem
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Очищаем корзину
            cart.items.all().delete()

            messages.success(request, f"Ваш заказ #{order.id} успешно оформлен!")
            return redirect('orders:order_detail', order_id=order.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                initial = {
                    'phone': profile.phone,
                    'address': profile.address
                }
            except Profile.DoesNotExist:
                pass
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form
    })


@login_required
@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    try:
        new_quantity = int(request.POST.get('quantity'))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()
    except (ValueError, TypeError):
        pass  # Оставляем прежнее количество при ошибке
    
    return redirect('cart:cart_detail')