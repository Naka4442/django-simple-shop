from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div


class OrderForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Адрес доставки', widget=forms.Textarea)
    phone = forms.CharField(label='Телефон', max_length=20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control-lg'),  # Увеличенное поле
            Field('email', placeholder='example@mail.com'),
            Div('address', css_class='mb-4'),  # Дополнительный отступ
            Submit('submit', 'Отправить', css_class='btn-success')
        )