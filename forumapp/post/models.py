from django.db import models
#from django.contrib.auth.models import Post
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=80)
    user = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    likes = models.ManyToManyField(Post, related_name='forum_post_likes')
    dislikes = models.ManyToManyField(Post, related_name='forum_post_dislikes')
    votes = models.IntegerField(default= 0)

def __str__(self):
    return self.title


# Create your models here.
