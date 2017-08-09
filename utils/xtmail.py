# coding:utf-8
from django.core import mail
from utils.captcha.xtcaptcha import Captcha
from django.core.cache import cache
from r_blog.settings import EMAIL_HOST_USER

def send_mail(request,email,check_data=None,subject=None,message=None):
    Captcha.number=6
    if not check_data:
        check_data=Captcha.gene_text()
    cache.set(email,check_data.lower(),10*60)
    Captcha.number = 4
    if not subject:
        subject=u'邮箱验证'
    if not message:
        message=u'尊敬的用户,您的邮箱验证码为: %s 验证码10分钟内有效' %check_data
    recipient_list=[email]
    from_email=EMAIL_HOST_USER

    if mail.send_mail(subject=subject,from_email=from_email,recipient_list=recipient_list,message=message):
        return True
    else:
        return False
