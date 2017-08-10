# coding:utf-8
from django.conf.urls import url
from . import views as cms_view

urlpatterns=[
    url(r'^$',cms_view.index,name='cms_index'),
    url(r'^login/$',cms_view.cms_login,name='cms_login'),
    url(r'^logout/$',cms_view.cms_logout,name='cms_logout'),
    url(r'^settings/',cms_view.settings,name="cms_settings"),
    url(r'^edit_email/',cms_view.edit_email,name="cms_edit_email"),
    url(r'^captcha_email/',cms_view.captcha_email,name="cms_captcha_email"),
    url(r'^add_article/$',cms_view.add_article,name="cms_add_article"),
    url(r'^edit_article/(?P<article_id>[\w\-]+)/$',cms_view.edit_article,name="cms_edit_article"),
    url(r'^add_category/$',cms_view.add_category,name="cms_add_category"),
    url(r'^add_tag/$',cms_view.add_tag,name="cms_add_tag"),
]