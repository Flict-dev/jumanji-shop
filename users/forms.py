from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Почта')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'email',
        )
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Почта',
            'password1': 'Пароль',
            'password2': 'Потверждение пароля',
        }
