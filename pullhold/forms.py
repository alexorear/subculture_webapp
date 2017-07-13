from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ComicTitle, Publisher
from django import forms


class UserForm(forms.ModelForm):
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    email = forms.EmailField(required = True)

    password = forms.CharField(widget = forms.PasswordInput())
    password_confirm = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ComicTitleForm(forms.ModelForm):
    class Meta:
        model = ComicTitle
        fields = ['comic_title', 'publisher', 'cover_art']
