from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, default=0, on_delete=models.CASCADE)    
    image = models.ImageField( upload_to="images")

    def __str__(self):
        return '%s' % (self.user)




# Create your models here.
