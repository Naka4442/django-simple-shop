from django import forms
from django.core.validators import RegexValidator
from .models import Order

class CheckoutForm(forms.ModelForm):
    phone = forms.CharField(
        label="Телефон",
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Формат: +79991234567")],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = ['address', 'phone', 'payment_method', 'comment']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
