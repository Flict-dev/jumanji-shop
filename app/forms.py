from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from app.models import Review, Order


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('stars', 'text')
        labels = {
            'stars': 'Оценка',
            'text': 'Отзыв'
        }


class OrderForm(ModelForm):
    comment = forms.CharField(required=False, widget=forms.Textarea)
    date_at = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'email',
            'date_at',
            'comment',
        )
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Телефон',
            'address': 'Адресс доставки',
            'email': 'Почта',
            'date_at': 'Число доставки',
            'comment': 'Комментарий к заказу',
        }
