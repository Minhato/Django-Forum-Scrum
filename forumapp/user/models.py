from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.contrib import admin


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, default=0, on_delete=models.CASCADE)    
    image = models.ImageField( upload_to="images")
    department = models.CharField(max_length=100, blank=True) 
    
    def __str__(self):
        return '%s' % (self.user)

from django.db.models.signals import post_save
from django.dispatch import receiver    
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


# Create your models here.
