from django.shortcuts import render
from utils.captcha.xtcaptcha import Captcha
from django.core.cache import cache
from django.http import HttpResponse,JsonResponse
try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO
import qiniu
from r_blog.settings import QINIU_ACCESS_KEY,QINIU_SECRET_KEY,BUCKET_NAME
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
# Create your views here.

def index(request):
    return HttpResponse('**')

def graph_captcha(request):
    text,image=Captcha.gene_code()
    cache.set(text.lower(),text.lower())
    out=StringIO()
    image.save(out,'png')
    out.seek(0)
    response=HttpResponse(content_type='image/png')
    response.write(out.read())
    return response

@login_required
@require_http_methods(['GET'])
def get_token(request):
    q=qiniu.Auth(QINIU_ACCESS_KEY,QINIU_SECRET_KEY)

    bucket_name=BUCKET_NAME

    token=q.upload_token(bucket_name)

    return JsonResponse(dict(uptoken=token))