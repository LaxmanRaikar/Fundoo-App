
from django.contrib.postgres.fields import ArrayField

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.urls import reverse


class  UserProfileInfo(models.Model):
    user = models.CharField(max_length=30)

    def __str__(self):
        return self.user


class Notes(models.Model):

    title = models.CharField(max_length=150, null=True)
    description = models.TextField(null=True)
    created_time = models.DateTimeField(auto_now_add=True,null=True)
    remainder = models.DateTimeField(default=None,null=True, blank=True)
    is_archived = models.BooleanField(default=False,null=True)
    is_deleted = models.BooleanField(default=False)
    color = models.CharField(default=None, max_length=50, blank=True, null=True)
    image = models.ImageField(default=None,null=True)
    trash = models.BooleanField(default=False)
    is_pinned = models.NullBooleanField(blank=True, null=True, default=None)
    labels = ArrayField(models.CharField(max_length=150,null=True,default=None),null=True,default=None)

    collaborate = models.ManyToManyField(User, null=True, blank=True, related_name='collaborated_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)

    def __str__(self):
        return self.title


class filepath(models.Model):
       filename = models.CharField(max_length= 200, null=True)



       def __str__(self):
           return  self.filename






