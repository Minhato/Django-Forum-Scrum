from django import forms
from django.contrib.auth.models import User
from .models import Post #,Author

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

class UpdateForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username']

