from django.db import models
from tinymce.models import HTMLField
from user.models import User

# Attributes for post are defined
class Post(models.Model):
    title = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=1500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='forum_post_likes')
    dislikes = models.ManyToManyField(User, related_name='forum_post_dislikes')
    votes = models.IntegerField(default= 0)
    image = models.ImageField( blank = True, null = True, upload_to = 'image/%Y/%m/%D')

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return '%s | posted by  %s' % (self.title, self.user)

# Attributes for comment are defined
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')
    likes = models.ManyToManyField(User, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes')
    votes = models.IntegerField(default= 0)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return 'Comment Content: %s | by %s | on POST: %s' % (self.comment_content, self.user, self.post.title)
