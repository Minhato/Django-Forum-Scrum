from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Post(models.Model):
    title = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return '%s | posted by  %s' % (self.title, self.user)

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, default=1, on_delete=models.CASCADE)    
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return '%s' % (self.user)

class Comment(models.Model):    
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.CharField(max_length=20)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment by %s on %s' % (self.user, self.post.title)
# Create your models here.
