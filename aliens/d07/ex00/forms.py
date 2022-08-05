from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Article


class Login(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'login',
        'autocomplete': 'off'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'password',
        'autocomplete': 'off'
    }))


class Signup(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class PublishForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'created']
        fields = ['title', 'synopsis', 'content']