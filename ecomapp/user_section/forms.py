from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
