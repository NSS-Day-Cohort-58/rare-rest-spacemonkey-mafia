from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractBaseUser, UserManager


class RareUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    author = models.ForeignKey("Author", on_delete=models.CASCADE,null=True, blank=True)
    # objects =  UserManager()