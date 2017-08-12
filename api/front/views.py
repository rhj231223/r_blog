#coding:utf-8
from django.shortcuts import render,redirect,reverse
from article.models import CategoryModel,ArticleModel,TagModel,TopModel
from utils.pagination import pagination
from r_blog.settings import SINGLE_PAGE_NUM,SHOW_PAGE
from utils import xtjson
from django.db.models import Count
from django.http import HttpResponse
# Create your views here.
def index(request):
    return article_list(request)

def article_list(request,page=1,category_id=0):
    page=int(page)
    category_id=int(category_id)
    articles = ArticleModel.objects.filter(is_remove=False).order_by('-create_time').all()
    top_articles=None
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
                       current_category=current_category,current_page=page,total_page=total_page)
        return render(request,'front_article_list.html',context=context)

def article_detail(request,article_id):
    article=ArticleModel.objects.filter(id=article_id).first()
    if not article:
        return HttpResponse(u'该文章没有找到')
    else:
        categorys = CategoryModel.objects.annotate(article_counts=Count('articlemodel')).order_by(
            '-article_counts').all()
        context=dict(categorys=categorys,article=article)
        return render(request,'front_article_detail.html',context=context)

def front_login(request):
    return render(request,'front_login.html')

def front_regist(request):
    return render(request,'front_regist.html')