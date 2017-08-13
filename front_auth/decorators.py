# coding:utf-8
from functools import wraps
from configs import FRONT_SESSION_ID
from django.shortcuts import redirect,reverse

def front_login_required(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if request.session.get(FRONT_SESSION_ID):
            return func(request,*args,**kwargs)
        else:
            return '%s?next=%s' %(redirect(reverse('front_login')),request.path)
    return wrapper