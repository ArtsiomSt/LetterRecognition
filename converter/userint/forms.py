from django import forms
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(), label='Password')


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(), label='Repeat password')