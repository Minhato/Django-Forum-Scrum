from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Comment, Post

# Form for post is defined
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'col': 50, 'class': 'form-control'}),           
        }

# Form for comment is defined
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =["post", "user", "comment_content"]
