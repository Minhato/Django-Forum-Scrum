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
    likes = models.ManyToManyField(User, related_name='forum_post_likes')
    dislikes = models.ManyToManyField(User, related_name='forum_post_dislikes')
    votes = models.IntegerField(default= 0)
    image = models.ImageField(blank = True, null = True, upload_to = 'image/%Y/%m/%D')

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return '%s | posted by  %s' % (self.title, self.user)

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, default=1, on_delete=models.CASCADE)    
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return '%s' % (self.user)

class Comment(models.Model):    
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return '%s by %s on %s' % (self.comment_content, self.user, self.post.title)
