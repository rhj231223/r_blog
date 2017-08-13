from __future__ import unicode_literals

from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from front_auth.models import FrontUserModel

# Create your models here.
class ArticleModel(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4)
    title=models.CharField(max_length=100)
    desc=models.CharField(max_length=100,blank=True)
    thumbnail=models.URLField(max_length=200,blank=True)
    content_html=models.TextField()
    create_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)
    read_count=models.IntegerField(default=0)
    is_remove=models.IntegerField(default=0)

    author=models.ForeignKey(User)
    category=models.ForeignKey('CategoryModel')
    tags=models.ManyToManyField('TagModel')
    top=models.OneToOneField('TopModel',null=True,on_delete=models.SET_NULL)


class CategoryModel(models.Model):
    name=models.CharField(max_length=30,unique=True)

class TagModel(models.Model):
    name=models.CharField(max_length=30,unique=True)

class TopModel(models.Model):
    create_time=models.DateTimeField(auto_now_add=True)

class CommentModel(models.Model):
    content=models.CharField(max_length=200)
    create_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)

    article=models.ForeignKey('ArticleModel')
    author=models.ForeignKey(FrontUserModel)

