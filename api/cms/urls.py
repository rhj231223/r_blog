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
]