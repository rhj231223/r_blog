# coding:utf-8
def avatar_context_processor(request):
    if hasattr(request,'cms_user'):
        cms_user=getattr(request,'cms_user')
        return dict(cms_user=cms_user)
    else:
        return {}