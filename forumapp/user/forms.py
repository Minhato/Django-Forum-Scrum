from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    department = forms.CharField(max_length=30, required=True, help_text='Please enter your department.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'department', 'password1', 'password2', )