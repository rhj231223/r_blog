from __future__ import unicode_literals

from django.db import models
from uuid import uuid4
from hash_helper import HashHelper

# Create your models here.

class FrontUserModel(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True)
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100)
    _password=models.CharField(max_length=200)
    join_time=models.DateTimeField(auto_now_add=True)
    avatar=models.URLField(blank=True)
    is_active=models.IntegerField(default=1)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_pwd):
        self._password=HashHelper.hash_password(raw_pwd)

    def check_pwd(self,raw_pwd):
        return HashHelper.check_password(raw_pwd=raw_pwd,hash_pwd=self.password)

