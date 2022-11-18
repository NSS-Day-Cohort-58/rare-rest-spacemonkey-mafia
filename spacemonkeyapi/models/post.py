from django.db import models

class Post(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=155)
    publication_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    image_url = models.URLField(max_length=200)
    content = models.CharField(max_length=155)
    approved =  models.BooleanField()
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="posts")
    
    tags = models.ManyToManyField("Tag", through="PostTag" )

    @property 
    def is_author(self):
        return self.__author

    @is_author.setter
    def is_author(self, value):
        self.__author = value
