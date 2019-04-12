# encoding: utf-8

from rest_framework import serializers
from .models import News, Comment
from apps.cms.models import NewsCategroy
from apps.xfzauth.serializers import authorSerializers
from apps.news.models import Banners


class NewsCategroySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategroy
        fields = ('id', 'name')


class NewsSerializers(serializers.ModelSerializer):
    categroy = NewsCategroySerializers()
    author = authorSerializers()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'pub_tiem', 'categroy', 'author')


class BannersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = ('id', 'priority', 'link_to', 'image_url')


class CommentSerializers(serializers.ModelSerializer):
    author = authorSerializers()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'pub_time')
