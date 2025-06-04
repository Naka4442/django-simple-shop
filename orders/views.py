from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from users.models import Profile
from django.contrib.auth.models import User
from .forms import CheckoutForm

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user) if request.user.is_authenticated else None

    if request.user.is_authenticated and not cart.items.exists():
        messages.warning(request, "Ваша корзина пуста")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user
            else:
                email = request.POST.get('email')
                if request.POST.get('create_account'):
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "Пользователь с таким email уже существует")
                        return render(request, 'orders/checkout.html', {'form': form})
                    password = User.objects.make_random_password()
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=request.POST.get('first_name'),
                        last_name=request.POST.get('last_name')
                    )
                    Profile.objects.create(user=user, phone=form.cleaned_data['phone'], address=form.cleaned_data['address'])
                    order.user = user

            order.total = cart.total_price() if cart else 0
            order.save()

            if cart:
                for item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                cart.items.all().delete()

            messages.success(request, f"Заказ #{order.id} успешно оформлен!")
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})