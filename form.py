from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.models import User
from django import forms

class CustomUserForm(UserCreationForm):
  username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'Enter your name'}))
  email = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'Enter your e-mail'}))
  password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Enter your password'}))
  password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Confirm your password'}))
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
    