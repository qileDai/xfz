#encoding:utf-8

from django import forms
from apps.forms import FormMixin

class publicCommentForm(forms.Form,FormMixin):
    content = forms.CharField()
    news_id = forms.IntegerField()