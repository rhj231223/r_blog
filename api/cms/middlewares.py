# coding:utf-8
from functools import wraps
from cms_auth.models import CMSUserModel

def avatar_middleware(get_response):
    def wrapper(request):
        if hasattr(request,'user'):
            cms_user = CMSUserModel.objects.filter(user_id=request.user.id).first()
            if cms_user:
                setattr(request,'cms_user',cms_user)
            return get_response(request)
    return wrapper