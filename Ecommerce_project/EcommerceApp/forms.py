from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class Registerform(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class SingupFrom(UserCreationForm):
    class Meta:
        model= User
        fields= ('username', 'email', 'first_name', 'last_name', 'password' )