from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Post(models.Model):
    title = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='forum_post_likes')
    dislikes = models.ManyToManyField(User, related_name='forum_post_dislikes')
    votes = models.IntegerField(default= 0)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, default=1, on_delete=models.CASCADE)    
    image = models.ImageField(upload_to="images")

class Comment(models.Model):    
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.CharField(max_length=20)
    body = models.TextField()

# Create your models here.
