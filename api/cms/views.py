#coding:utf-8
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from forms import LoginForm,SettingsForm,\
    SendEmailForm,EditEmailForm,AddCategoryForm,\
    AddTagForm,AddArticleForm,TopArticleForm,\
    DeleteArticleForm,EditCategoryForm,DeleteCategoryForm
from utils import xtjson
from cms_auth.models import CMSUserModel
from utils.xtmail import send_mail
from article.models import ArticleModel,\
CategoryModel,TagModel,TopModel
from utils.pagination import pagination
from r_blog.settings import SINGLE_PAGE_NUM,SHOW_PAGE
from django.db.models import Count
# Create your views here.

@login_required
@require_http_methods(['GET'])
def index(request):
    return article_manage(request,page=1,category_id=0)

@login_required
@require_http_methods(['GET'])
def article_manage(request,page=1,category_id=0):
    page=int(page)
    category_id=int(category_id)
    articles=ArticleModel.objects.order_by('-top__create_time','-create_time').all()
    categorys=CategoryModel.objects.all()

    if category_id!=0:
        articles=articles.filter(category_id=category_id)

    total_page,start,end,page_list=pagination(page,articles.count(),SINGLE_PAGE_NUM,SHOW_PAGE)
    context=dict(articles=articles[start:end],categorys=categorys,
                 current_page=page,current_category_id=category_id,
                 total_page=total_page,page_list=page_list)
    return render(request,'cms_article_manage.html',context=context)

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


def cms_logout(request):
    logout(request)
    return redirect(reverse('cms_login'))

@login_required
@require_http_methods(['GET','POST'])
def settings(request):
    if request.method=='GET':
        return render(request,'cms_settings.html')
    else:
        form=SettingsForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            avatar=form.cleaned_data.get('avatar')

            user=request.user
            cms_user=request.cms_user
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


@login_required
@require_http_methods(['GET','POST'])
def add_article(request):
    if request.method=='GET':
        categorys=CategoryModel.objects.all()
        tags=TagModel.objects.all()
        context=dict(categorys=categorys,tags=tags)
        return render(request,'cms_add_article.html',context=context)
    else:
        form=AddArticleForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data.get('title')
            category_id=form.cleaned_data.get('category_id')
            desc=form.cleaned_data.get('desc')
            thumbnail=form.cleaned_data.get('thumbnail')
            content_html=form.cleaned_data.get('content_html')
            tags=request.POST.getlist('tags[]')

            category=CategoryModel.objects.filter(id=category_id).first()
            article=ArticleModel(title=title,desc=desc,content_html=content_html)

            if desc:
                article.desc=desc
            if thumbnail:
                article.thumbnail=thumbnail

            article.category = category
            article.author = request.user

            article.save()
            if tags:
                for tag_id in tags:
                    tag=TagModel.objects.filter(id=tag_id).first()
                    article.tags.add(tag)
            return xtjson.json_result()

        else:
            return form.get_error_response()

@login_required
@require_http_methods(['GET','POST'])
def edit_article(request,article_id):
    article = ArticleModel.objects.filter(id=article_id).first()
    if request.method=='GET':
        categorys=CategoryModel.objects.all()
        tags=TagModel.objects.all()
        current_category=article.category
        current_tag_ids=[tag.id for tag in article.tags.all()]
        context=dict(article=article,categorys=categorys,tags=tags,
                     current_category=current_category,
                     current_tag_ids=current_tag_ids)
        return render(request,'cms_edit_article.html',context=context)
    else:
        form=AddArticleForm(request.POST)
        if form.is_valid():
            if article:
                # title=form.cleaned_data.get('title')
                # desc=form.cleaned_data.get('desc')
                # thumbnail=form.cleaned_data.get('thumbnail')
                # content_html=form.cleaned_data.get('content_html')
                category_id=form.cleaned_data.get('category_id')
                tags=request.POST.getlist('tags[]')

                for k,v in form.cleaned_data.iteritems():
                    if k!='category_id':
                        setattr(article,k,v)

                category=CategoryModel.objects.filter(id=category_id).first()
                article.category=category
                article.save()

                if tags:
                    article.tags.set([])
                    for tag_id in tags:
                        tag=TagModel.objects.filter(id=tag_id).first()
                        article.tags.add(tag)
                return xtjson.json_result()


            else:
                return xtjson.json_params_error(message=u'没有找到该文章!')
        else:
            return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def add_category(request):
    form=AddCategoryForm(request.POST)
    if form.is_valid():
        category_name=form.cleaned_data.get('category_name')
        db_category=CategoryModel.objects.filter(name=category_name).first()
        if not db_category:
            category=CategoryModel(name=category_name)
            category.save()
            return xtjson.json_result(data=dict(id=category.id,name=category.name))
        else:
            return xtjson.json_params_error(message=u'已经有同名的分类了,无需添加!')
    else:
        return form.get_error_response()

@login_required
@require_http_methods(['POST'])
def add_tag(request):
    form=AddTagForm(request.POST)
    if form.is_valid():
        tag_name=form.cleaned_data.get('tag_name')
        db_tag=TagModel.objects.filter(name=tag_name).first()
        if not db_tag:
            tag=TagModel(name=tag_name)
            tag.save()
            return xtjson.json_result(data=dict(id=tag.id,name=tag.name))
        else:
            return xtjson.json_params_error(message=u'已经有同名的标签了,无需添加!')

    else:
        return form.get_error_response()

@login_required
@require_http_methods(['POST'])
def top_article(request):
    form=TopArticleForm(request.POST)
    if form.is_valid():
        article_id=form.cleaned_data.get('article_id')
        is_top=form.cleaned_data.get('is_top')

        if not article_id:
            return xtjson.json_params_error(message=u'请指定文章id!')
        else:
            article=ArticleModel.objects.filter(id=article_id).first()
            if not article:
                return xtjson.json_params_error(message=u'该文章不存在!')
            else:
                if not article.top:
                    if article.thumbnail:
                        if is_top==1:
                            top=TopModel()
                            top.save()
                            article.top=top
                            article.save(update_fields=['top'])
                            return xtjson.json_result()
                        else:
                            return xtjson.json_params_error(message=u'该文章已置顶,无需重复置顶!')
                    else:
                        return xtjson.json_params_error(message=u'置顶的文章必须有缩略图!')
                else:
                    if is_top==0:
                        article.top.delete()

                        return xtjson.json_result()
                    else:
                        return xtjson.json_params_error(message=u'该文章没有置顶，无需取消置顶')
    else:
        return form.get_error_response()

@login_required
@require_http_methods(['POST'])
def delete_article(request):
    form=DeleteArticleForm(request.POST)
    if form.is_valid():
        article_id=form.cleaned_data.get('article_id')
        is_remove=form.cleaned_data.get('is_remove')
        if not article_id:
            return xtjson.json_params_error(message=u'必须指定文章ID!')
        else:
            article=ArticleModel.objects.filter(id=article_id).first()
            if not article:
                return xtjson.json_params_error(message=u'没有找到该文章!')
            else:
                if not article.is_remove:
                    if is_remove==1:
                        article.is_remove=1
                        article.save()
                        return xtjson.json_result()
                    else:
                        return xtjson.json_params_error(message=u'该文章没有被删除,无需取消删除!')
                else:
                    if is_remove==0:
                        article.is_remove=0
                        article.save()
                        return xtjson.json_result()
                    else:
                        return xtjson.json_params_error(message=u'该文章已被删除，无需重复删除!')
    else:
        return form.get_error_response()

@login_required
@require_http_methods(['GET'])
def category_manage(request):
    categorys=CategoryModel.objects.annotate(article_counts=Count('articlemodel')).order_by('-article_counts').all()
    context=dict(categorys=categorys)
    return render(request,'cms_category_manage.html',context=context)

@login_required
@require_http_methods(['POST'])
def edit_category(request):
    form=EditCategoryForm(request.POST)
    if form.is_valid():
        category_id=form.cleaned_data.get('category_id')
        category_name=form.cleaned_data.get('category_name')
        if not category_id:
            return xtjson.json_params_error(message=u'请指定分类ID')
        else:
            category=CategoryModel.objects.filter(id=category_id).first()
            if not category:
                return xtjson.json_params_error(u'没有找到该文章!')
            else:
                db_category=CategoryModel.objects.filter(name=category_name).first()
                if db_category and db_category!=category:
                    return xtjson.json_params_error(message=u'已经有同名的分类了!')
                else:
                    category.name=category_name
                    category.save()
                    return xtjson.json_result()
    else:
        return form.get_error_response()

@login_required
@require_http_methods(['POST'])
def delete_category(request):
    form=DeleteCategoryForm(request.POST)
    if form.is_valid():
        category_id=form.cleaned_data.get('category_id')
        if not category_id:
            return xtjson.json_params_error(message=u'必须指定分类ID')
        else:
            category=CategoryModel.objects.filter(id=category_id).first()
            if not category:
                return xtjson.json_params_error(message=u'没有找到该文章!')
            elif category.articlemodel_set.count():
                return xtjson.json_params_error(message=u'该分类下还有文章,不能删除!')
            else:
                category.delete()
                return xtjson.json_result()
    else:
        return form.get_error_response()

def test(request):
    category=CategoryModel.objects.first()
    author=User.objects.first()
    tags=TagModel.objects.all()[1:4]

    for i in xrange(100):
        title='标题 %s' %i
        content_html='内容 %s' %i

        article=ArticleModel(title=title,content_html=content_html)
        article.category=category
        article.author=author
        article.save()
        article.tags.set(tags)
    return HttpResponse('success')