# coding:utf-8
from django import forms
from utils import xtjson
from django.core.cache import cache

class BaseForm(forms.Form):
    def get_one_error(self):
        k,v=self.errors.popitem()
        message=v[0]
        return message

    def get_errors(self):
        li=[ '*'.join(v) for k,v in self.errors.iteritems()]
        message='*'.join(li)
        return message

    def get_error_response(self):
        if self.errors:
            return xtjson.json_params_error(message=self.errors.as_text())


class GraphCaptchaForm(BaseForm):
    graph_captcha=forms.CharField(min_length=4,max_length=4)

    def clean_graph_captcha(self):
        captcha=self.cleaned_data.get('graph_captcha')
        cache_captcha=cache.get(captcha.lower())

        if not cache_captcha or captcha.lower()!=cache_captcha.lower():
            self.add_error('graph_captcha',u'验证码输入有误!')
        else:
            return captcha