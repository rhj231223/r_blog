# coding:utf-8
from django.db import models
from django.contrib.auth.models import User

class CMSUserModel(models.Model):
    avatar=models.CharField(max_length=200,blank=True)

    user=models.OneToOneField(User)