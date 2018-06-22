from __future__ import unicode_literals
from django.db import models
import re
from django.http import HttpResponse
from django.contrib import messages
import datetime

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=75)
    date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name

class Wishlist(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey("User", related_name="creator", on_delete="CASCADE")
    users = models.ManyToManyField(User, related_name="users")
    created_at = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return self.name
