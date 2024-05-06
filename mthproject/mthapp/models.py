from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime, timezone

User =get_user_model()



# Create your models here.
class NewManager(models.Manager):
    pass


class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    moviename = models.CharField(max_length=100, default="", null=True)
    descriptions = models.CharField(max_length=200, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default="")
    actors_name = models.TextField(default="")
    youtube_link = models.URLField(default="")
    images = models.ImageField(upload_to='post_images')
    rdate = models.DateField()
    created_date = models.DateTimeField(default=datetime.now)
    favourites = models.ManyToManyField(User, related_name='favourites', default=None,blank=True)
    objects = models.Manager() # default manager
    newmanager = NewManager() # new manager

    def __str__(self):
        return self.author.username

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField(default=True, primary_key=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', default='images/blankprofile.png')


    def __str__(self):
        return self.user.username
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=150,default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.moviename,str(self.author.username))

