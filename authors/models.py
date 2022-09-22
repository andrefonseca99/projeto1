from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=165, default='', blank=True)
    contact = models.TextField(max_length=65, default='', blank=True)
