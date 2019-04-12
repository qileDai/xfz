from django.db import models


# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_tiem =  models.DateTimeField(auto_now_add=True)
    categroy = models.ForeignKey('cms.NewsCategroy',on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey('xfzauth.User',on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering = ['-pub_tiem']


class Banners(models.Model):
    priority = models.IntegerField()
    image_url = models.URLField()
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority']

class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('News',on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey('xfzauth.User',on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']





