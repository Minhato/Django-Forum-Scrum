from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=80)

    def __str__(self):
        return self.name


# Create your models here.
