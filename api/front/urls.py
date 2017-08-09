# coding:utf-8
from django.conf.urls import url
from . import views as front_view

urlpatterns=[
    url(r'^$',front_view.index,name='front_index'),
]