from django.shortcuts import render, redirect
from .forms import OrderForm

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Обработка данных
            return redirect('success_page')
    else:
        form = OrderForm()
    return render(request, 'orders/create.html', {'form': form})