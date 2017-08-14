# coding:utf-8
from django import forms
from api.common.forms import BaseForm,GraphCaptchaForm

class FrontLoginForm(GraphCaptchaForm):
    email=forms.EmailField()
    password=forms.CharField(min_length=6,max_length=20)
    remember=forms.IntegerField(required=False)

class FrontRegistForm(GraphCaptchaForm):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, max_length=20)
    username=forms.CharField(min_length=3,max_length=12)

class AddComentForm(BaseForm):
    content=forms.CharField(max_length=200)
    article_id=forms.UUIDField()

class EditCommentForm(AddComentForm):
    comment_id=forms.CharField(max_length=100)

class ReplyCommentForm(BaseForm):
    content=forms.CharField(max_length=200)