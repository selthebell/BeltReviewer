# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Author(models.Model):
     first_name = models.CharField(max_length=45)
     last_name = models.CharField(max_length=45)
     created_at = models.DateTimeField(auto_now_add = True)
     updated_at = models.DateTimeField(auto_now = True)

class Books(models.Model):
    title = models.CharField(max_length=50)
    #author=models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    published_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category=models.CharField(max_length=25)
    def __str__(self):
        return "title :"+self.title+"publishes date :"+str(self.published_date)
