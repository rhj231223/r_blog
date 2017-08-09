#coding:utf-8
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from forms import LoginForm,SettingsForm,\
    SendEmailForm,EditEmailForm
from utils import xtjson
from cms_auth.models import CMSUserModel
from utils.xtmail import send_mail
# Create your views here.

@login_required
@require_http_methods(['GET'])
def index(request):
    return render(request,'cms_base.html')

@require_http_methods(['GET','POST'])
def cms_login(request):
    if request.method=='GET':
        return render(request,'cms_login.html')
    else:
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            remember=form.cleaned_data.get('remember')
            user=authenticate(username=username,password=password)
            if user:
                login(request, user)
                if remember:
                    request.session.set_expiry(86400*30)
                else:
                    request.session.set_expiry(0)

                next_url=request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(reverse('cms_index'))
            else:
                context = dict(message=u'账号或密码错误!')

        else:
            context=dict(message=form.errors.as_text())
        return render(request,'cms_login.html',context=context)

@login_required
def cms_logout(request):
    logout(request)
    return redirect(reverse('cms_login'))

@login_required
@require_http_methods(['GET','POST'])
def settings(request):
    cms_user=CMSUserModel.objects.filter(user_id=request.user.id).first()
    if request.method=='GET':
        context=dict(cms_user=cms_user)
        return render(request,'cms_settings.html',context=context)
    else:
        form=SettingsForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            avatar=form.cleaned_data.get('avatar')

            user=request.user
            if cms_user:
                cms_user.avatar=avatar
                cms_user.save()
            else:
                cms_user=CMSUserModel(avatar=avatar)
                cms_user.user=user
                cms_user.save()
            user.username = username
            user.save()
            return xtjson.json_result()
        else:
            return form.get_error_response()

@login_required
def edit_email(request):
    if request.method=='GET':
        return render(request,'cms_edit_email.html')
    else:
        form=EditEmailForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            user=request.user

            user.email = email
            user.save(update_fields=['email'])
            return xtjson.json_result()
        else:
            return form.get_error_response()

@login_required
@require_http_methods(['POST'])
def captcha_email(request):
    form=SendEmailForm(request.POST)
    if form.is_valid():
        email=form.cleaned_data.get('email')
        if email==request.user.email:
            return xtjson.json_params_error(message=u'新旧密码一致,无需修改啊')
        if send_mail(request,email):
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=u'邮件发送失败,请检查邮箱填写是否有误')
    else:
        return form.get_error_response()