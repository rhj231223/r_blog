#coding:utf-8
from django.shortcuts import render,redirect,reverse
from article.models import CategoryModel,ArticleModel,CommentModel
from utils.pagination import pagination
from r_blog.settings import SINGLE_PAGE_NUM,SHOW_PAGE
from utils import xtjson
from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from forms import FrontLoginForm,FrontRegistForm,\
    AddComentForm,EditCommentForm,ReplyCommentForm
from front_auth.models import FrontUserModel
from front_auth.configs import FRONT_SESSION_ID
from front_auth.decorators import front_login_required
from django.db.models import Q

# Create your views here.
def index(request):
    return article_list(request)

def article_list(request,page=1,category_id=0):
    page=int(page)
    category_id=int(category_id)
    articles = ArticleModel.objects.filter(is_remove=False).order_by('-create_time').all()
    top_articles=None
    query=request.GET.get('query')
    if query:
        articles=articles.filter(Q(title__icontains=query)|Q(content_html__icontains=query))
    else:

        if category_id:
            articles=articles.filter(category_id=category_id)
        else:
            old_articles=articles
            articles=old_articles.filter(top__isnull=True)
            top_articles = old_articles.filter(top__isnull=False)

    total_page,start,end,page_list=pagination(page,articles.count(),SINGLE_PAGE_NUM,SHOW_PAGE)
    articles=list(articles.values()[start:end])
    print total_page
    context=dict(articles=articles,current_page=page)

    if request.is_ajax():
        return xtjson.json_result(data=context)
    else:
        categorys = CategoryModel.objects.annotate(article_counts=Count('articlemodel')).order_by('-article_counts').all()
        current_category = CategoryModel.objects.filter(id=category_id).first()
        context = dict(articles=articles,categorys=categorys,top_articles=top_articles,
                       current_category=current_category,current_page=page,total_page=total_page,query=query)
        return render(request,'front_article_list.html',context=context)

def detail_base(request,article_id):
    article = ArticleModel.objects.filter(id=article_id).first()
    if not article:
        return HttpResponse(u'该文章没有找到')
    else:
        categorys = CategoryModel.objects.annotate(article_counts=Count('articlemodel')).order_by(
            '-article_counts').all()
        comments = article.commentmodel_set.all()
        context = dict(categorys=categorys, article=article, comments=comments)
        return context

def article_detail(request,article_id):
    context=detail_base(request,article_id)
    return render(request,'front_article_detail.html',context)

@require_http_methods(['GET','POST'])
def front_login(request):
    if request.method=='GET':
        return render(request,'front_login.html')
    else:
        form=FrontLoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            remember=form.cleaned_data.get('remember')

            front_user=FrontUserModel.objects.filter(email=email).first()
            if not front_user:
                context=dict(message=u'帐号或密码错误!')
            else:
                if front_user.check_pwd(password):
                    request.session[FRONT_SESSION_ID]=str(front_user.id)
                    if remember:
                        request.session.set_expiry(86400*30)
                    else:
                        request.session.set_expiry(0)
                    next_url=request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect(reverse('front_index'))
                else:
                    context = dict(message=u'帐号或密码错误!')
        else:
            context=dict(message=form.errors.as_text())
        return render(request,'front_login.html',context=context)

@require_http_methods(['GET','POST'])
def front_regist(request):
    if request.method=='GET':
        return render(request,'front_regist.html')
    else:
        form=FrontRegistForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            username=form.cleaned_data.get('username')
            db_user=FrontUserModel.objects.filter(email=email).first()
            if not db_user:
                front_user=FrontUserModel(email=email,password=password,username=username)
                front_user.save()
                request.session[FRONT_SESSION_ID]=str(front_user.id)
                return redirect(reverse('front_index'))
            else:
                context=dict(message=u'该邮箱已经注册!')

        else:
            context=dict(message=form.error.as_text())
        return render(request,'front_regist.html',context=context)

@front_login_required
@require_http_methods(['POST'])
def add_comment(request):
    form=AddComentForm(request.POST)
    if form.is_valid():
        content=form.cleaned_data.get('content')
        article_id=form.cleaned_data.get('article_id')
        author=request.front_user

        article=ArticleModel.objects.filter(id=article_id).first()
        if article:
            comment=CommentModel(content=content)
            comment.article=article
            comment.author=author
            comment.save()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=u'没有找到该文章!')
    else:
        return form.get_error_response()

@front_login_required
@require_http_methods(['GET','POST'])
def edit_comment(request,article_id,comment_id):
    current_comment = CommentModel.objects.filter(id=comment_id).first()
    if request.method=='GET':
        context=detail_base(request,article_id)
        if current_comment:
            if current_comment.author.id!=request.front_user.id:
                context.update(message=u'您的权限不足')
            else:
                context=context.update(current_comment_id=comment_id, current_comment=current_comment)
        else:
            context.update(message=u'没有找到该评论!')
        return render(request, 'front_edit_comment.html', context=context)

    else:
        form=EditCommentForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data.get('content')
            comment_id=form.cleaned_data.get('comment_id')
            comment=CommentModel.objects.filter(id=comment_id).first()
            if comment:
                comment.content=content
                comment.save(update_fields=['content'])
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'没有找到该评论!')

        else:
            return form.get_error_response()

@front_login_required
@require_http_methods(['GET','POST'])
def reply_comment(request,article_id,comment_id):
    current_comment=CommentModel.objects.filter(id=comment_id).first()
    if request.method=='GET':
        context=detail_base(request,article_id)
        if current_comment:
            if current_comment.author.id==request.front_user.id:
                context.update(message=u'您无需回复自己的评论!')
            else:
                context.update(current_comment_id=comment_id,current_comment=current_comment)
        else:
            context.update(message=u'没有找到该评论!')
        return render(request,'front_reply_comment.html',context=context)
    else:
        form=ReplyCommentForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data.get('content')

            article=ArticleModel.objects.filter(id=article_id).first()
            author=request.front_user

            comment=CommentModel(content=content)
            comment.origin_comment=current_comment
            comment.article=article
            comment.author=author
            comment.save()
            return xtjson.json_result()
        else:
            return form.get_error_response()
def front_logout(request):
    request.session.pop(FRONT_SESSION_ID,None)
    return redirect(reverse('front_login'))


def test(request):
    pass