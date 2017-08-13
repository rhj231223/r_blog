# coding:utf-8

def front_user_context_processor(request):
    if hasattr(request,'front_user'):
        return dict(front_user=getattr(request,'front_user'))
    else:
        return {}