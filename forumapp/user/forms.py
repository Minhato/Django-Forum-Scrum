from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Post, Profile

class SignUpForm(UserCreationForm):
    letters = RegexValidator(r'^[a-zA-Z]+$', 'Only letter characters are allowed.')
    # erweitert um die Felder und erbt von UsercreationForm, nötig da UserCreation form nur Username und Passwort enthält.
    first_name = forms.CharField(max_length=30, required=True, help_text='required.', validators=[letters])
    #first_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
    last_name = forms.CharField(max_length=30, required=True, help_text='required.', validators=[letters]) 
    email = forms.EmailField(max_length=254, help_text='required. Enter a valid email address.')
    CHOICES = (('Option 1', 'IT'),('Option 2', 'Marketing'),('Option 3', 'Accounting'))
    department = forms.ChoiceField(choices=CHOICES)
    #department = forms.CharField(max_length=30, required=True, help_text='required')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]

class UpdateForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', )
