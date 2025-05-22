from django.urls import path
from .views import cart_add, cart_view

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add/<int:product_id>', cart_add, name='add_to_cart'),
]