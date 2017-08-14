from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
# Create your views here.

def index(request):
    pass

@require_http_methods(['POST'])
def test(request):
    return HttpResponse('success')


def test2(request):
    if request.method=='GET':
        return render(request, 'frontauth_test2.html')
    else:
        url=request.POST.get('url')
        return redirect(url)