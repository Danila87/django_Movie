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


class AuthenticationUserForm(AuthenticationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Danila87'
    }))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '*************'
    }))


class ReviewForm(forms.ModelForm):

    class Meta:

        model = models.Review
        fields = ['text_review', 'user_rating']

        labels = {
            'text_review': 'Текст рецензии: ',
            'user_rating': 'Ваша оценка фильму: '
        }

        widgets = {
            'text_review': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'user_rating': forms.NumberInput(attrs={'class': 'form-control col-2', 'min': 0, 'max': 10})
        }
