# coding:utf-8
from django.conf.urls import url
from . import views as front_view

urlpatterns=[
    url(r'^$',front_view.index,name='front_index'),
    url(r'^article_list/(?P<page>\d+)/(?P<category_id>\d+)/$',front_view.article_list,name='front_article_list'),
    url(r'^article_detail/(?P<article_id>[\w\-]+)/$',front_view.article_detail,name='front_article_detail'),
    url(r'^front_login/$',front_view.front_login,name='front_login'),
    url(r'^front_regist/$',front_view.front_regist,name='front_regist'),
]