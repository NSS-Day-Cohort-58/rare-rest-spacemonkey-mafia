from django.db import models



class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)    