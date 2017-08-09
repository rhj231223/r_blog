# coding:utf-8
from django.conf.urls import url
from . import views as common_view

urlpatterns=[
    url(r'^$',common_view.index,name='common_index'),
    url(r'^graph_captcha/$',common_view.graph_captcha,name="common_graph_captcha"),
    url(r'^get_token/$',common_view.get_token,name='common_get_token'),
]