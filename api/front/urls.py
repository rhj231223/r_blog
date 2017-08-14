# coding:utf-8
from django.conf.urls import url
from . import views as front_view

urlpatterns=[
    url(r'^$',front_view.index,name='front_index'),
    url(r'^article_list/(?P<page>\d+)/(?P<category_id>\d+)/$',front_view.article_list,name='front_article_list'),
    url(r'^article_detail/(?P<article_id>[\w\-]+)/$',front_view.article_detail,name='front_article_detail'),
    url(r'^login/$',front_view.front_login,name='front_login'),
    url(r'^regist/$',front_view.front_regist,name='front_regist'),
    url(r'^logout/$',front_view.front_logout,name='front_logout'),
    url(r'^add_comment/$',front_view.add_comment,name='front_add_comment'),
    url(r'^edit_comment/(?P<article_id>[\w\-]+)/(?P<comment_id>[\w\-]+)/$',front_view.edit_comment,name='front_edit_comment'),
    url(r'^reply_comment/(?P<article_id>[\w\-]+)/(?P<comment_id>[\w\-]+)/$',front_view.reply_comment,name='front_reply_comment'),
    url(r'^test/$',front_view.test,name='test'),
]