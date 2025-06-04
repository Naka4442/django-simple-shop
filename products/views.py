from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    return render(request, 'products/list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })