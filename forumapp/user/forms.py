from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Profile

# Form for user is defined
class SignUpForm(UserCreationForm):
    letters = RegexValidator(r'^[a-zA-Z]+$', 'Only letter characters are allowed.')
    # erweitert um die Felder und erbt von UsercreationForm, nötig da UserCreation form nur Username und Passwort enthält.
    first_name = forms.CharField(max_length=30, help_text='required.', validators=[letters])
    last_name = forms.CharField(max_length=30, help_text='required.', validators=[letters]) 
    email = forms.EmailField(max_length=254, help_text='required. Enter a valid email address.')
    CHOICES = (('IT', 'IT'),('Marketing', 'Marketing'),('Accounting', 'Accounting'))
    department = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'department')


class UpdateForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username']


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('image',)
		#exclude = ['department']
