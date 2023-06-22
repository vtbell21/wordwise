from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SentenceForm(forms.Form):
    sentence = forms.CharField(label='Enter a sentence', max_length=200)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
