# coding:utf-8
from django.conf.urls import url
from . import views as frontauth_view

urlpatterns=[
    url(r'^$',frontauth_view.index,name="frontauth_index"),
    url(r'^test/$',frontauth_view.test,name='frontauth_view_test'),
    url(r'^test2/$',frontauth_view.test2,name='frontauth_view_test2'),
]
