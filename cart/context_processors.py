def cart_items_count(request):
    count = 0
    if 'cart' in request.session:
        count = sum(request.session['cart'].values())
    return {'cart_items_count': count}