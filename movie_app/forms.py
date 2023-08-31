from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from . import models


class FormRegisterUser(UserCreationForm):

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Danila87'
    }))

    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Данила'
    }))

    last_name = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Сергеев'
    }))

    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'danila87@mail.ru'
    }))

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:

        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

