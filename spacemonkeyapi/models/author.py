from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=75, null=True, blank=True) 
    age = models.IntegerField(null=True, blank=True)
    bio = models.CharField(max_length=75)
