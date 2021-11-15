from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post #,Author

class SignUpForm(UserCreationForm):
    # erweitert um die Felder und erbt von UsercreationForm, nötig da UserCreation form nur Username und Passwort enthält.
    first_name = forms.CharField(max_length=30, required=True, help_text='required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    Department = forms.CharField(max_length=30, required=True, help_text='Please enter your department.')

    class Meta:
        #zum einfügen der neuen felder und Anordnung wie es später auf der html angezeigt werden soll
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'Department', 'password1', 'password2', )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

class UpdateForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username']
