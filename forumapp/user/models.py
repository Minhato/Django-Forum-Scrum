from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.core.validators import RegexValidator

#class Post(models.Model):
#    title = models.CharField(max_length=20, unique=True)
#    description = models.CharField(max_length=80)
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    content = HTMLField()
#    date = models.DateTimeField(auto_now_add=True)
#    date = models.DateTimeField(auto_now=True)
#    approved = models.BooleanField(default=False)
#    likes = models.ManyToManyField(User, related_name='forum_post_likes')
#    dislikes = models.ManyToManyField(User, related_name='forum_post_dislikes')
#    votes = models.IntegerField(default= 0)
#    image = models.ImageField(blank = True, null = True, upload_to = 'image/%Y/%m/%D')
#    def __str__(self):
#        return '%s | posted by  %s' % (self.title, self.user)

#class SignUp(models.Model):
#    letters = RegexValidator(r'^[a-zA-Z]+$', 'Only letter characters are allowed.')
#    # erweitert um die Felder und erbt von UsercreationForm, nötig da UserCreation form nur Username und Passwort enthält.
#    first_name = models.CharField(max_length=30, help_text='required.', validators=[letters])
#    #first_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
#    last_name = models.CharField(max_length=30, help_text='required.', validators=[letters]) 
#    email = models.EmailField(max_length=254, help_text='required. Enter a valid email address.')
#    CHOICES = (('Option 1', 'IT'),('Option 2', 'Marketing'),('Option 3', 'Accounting'))
    #department = models.ChoiceField(choices=CHOICES)


from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, default=1, on_delete=models.CASCADE)   
    #letters = RegexValidator(r'^[a-zA-Z]+$', 'Only letter characters are allowed.')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True) 
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return '%s' % (self.user)

    
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

#class Comment(models.Model):    
#    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
#    user = models.CharField(max_length=20)
#    body = models.TextField()
#    date = models.DateTimeField(auto_now_add=True)

#    def __str__(self):
#        return 'Comment by %s on %s' % (self.user, self.post.title)

#def __str__(self):
#    return self.title


# Create your models here.


#Add Extra Fields:
#https://dev.to/thepylot/create-advanced-user-sign-up-view-in-django-step-by-step-k9m 