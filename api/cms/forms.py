# coding:utf-8
from django import forms
from api.common.forms import BaseForm,GraphCaptchaForm
from django.core.cache import cache

class LoginForm(GraphCaptchaForm):
    username=forms.CharField(min_length=3,max_length=20)
    password=forms.CharField(min_length=6,max_length=20)
    remember=forms.IntegerField(required=False)

class SettingsForm(BaseForm):
    username=forms.CharField(min_length=3,max_length=12)
    avatar=forms.URLField(max_length=200)

class SendEmailForm(BaseForm):
    email=forms.EmailField()


class EditEmailForm(SendEmailForm):
    email_captcha=forms.CharField(min_length=6,max_length=6)

    def clean(self):
        email=self.cleaned_data.get('email')
        email_captcha=self.cleaned_data.get('email_captcha')
        cache_captcha=cache.get(email)

        if not cache_captcha or email_captcha.lower()!=cache_captcha.lower():
            self.add_error('email_captcha',u'邮件验证码错误!')
        else:
            return self.cleaned_data