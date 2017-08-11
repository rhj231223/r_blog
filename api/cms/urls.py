# coding:utf-8
from django.conf.urls import url
from . import views as cms_view

urlpatterns=[
    url(r'^$',cms_view.index,name='cms_index'),
    url(r'^article_manage/(?P<page>\d+)/(?P<category_id>\d+)/$',cms_view.article_manage,name='cms_article_manage'),
    url(r'^category_manage/$',cms_view.category_manage,name='cms_category_manage'),
    url(r'^login/$',cms_view.cms_login,name='cms_login'),
    url(r'^logout/$',cms_view.cms_logout,name='cms_logout'),
    url(r'^settings/',cms_view.settings,name="cms_settings"),
    url(r'^edit_email/',cms_view.edit_email,name="cms_edit_email"),
    url(r'^captcha_email/',cms_view.captcha_email,name="cms_captcha_email"),
    url(r'^add_article/$',cms_view.add_article,name="cms_add_article"),
    url(r'^edit_article/(?P<article_id>[\w\-]+)/$',cms_view.edit_article,name="cms_edit_article"),
    url(r'^add_category/$',cms_view.add_category,name="cms_add_category"),
    url(r'^add_tag/$',cms_view.add_tag,name="cms_add_tag"),
    url(r'^top_article/$',cms_view.top_article,name="cms_top_article"),
    url(r'^delete_article/$',cms_view.delete_article,name="cms_delete_article"),
    url(r'^edit_category/$',cms_view.edit_category,name="cms_edit_category"),
    url(r'^delete_category/$',cms_view.delete_category,name="cms_delete_category"),
    url(r'^test/$',cms_view.test,name='cms_test')
]