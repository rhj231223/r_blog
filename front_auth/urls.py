# coding:utf-8
from django.conf.urls import url
from . import views as frontauth_view

urlpatterns=[
    url(r'^$',frontauth_view.index,name="frontauth_index"),
]
