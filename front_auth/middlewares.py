# coding:utf-8
from configs import FRONT_SESSION_ID
from models import FrontUserModel

def front_user_middleware(get_response):
    def wrapper(request):
        user_id=request.session.get(FRONT_SESSION_ID,None)
        if user_id:
            front_user=FrontUserModel.objects.filter(id=user_id).first()
            if front_user:
                setattr(request,'front_user',front_user)
        return get_response(request)
    return wrapper