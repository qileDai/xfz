#encoding:utf-8

from django.db import models

class CourseCategroy(models.Model):
    name = models.CharField(max_length=100)

class Teacher(models.Model):
    username = models.CharField(max_length=100)
    avatar = models.URLField()
    jobtitle = models.CharField(max_length=100)
    profile = models.TextField()


class Course(models.Model):
    title = models.CharField(max_length=200)
    categroy = models.ForeignKey('CourseCategroy',on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher',on_delete=models.DO_NOTHING)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField()
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)

class CourseOrder(models.Model):
    course = models.ForeignKey("Course",on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey("xfzauth.User",on_delete=models.DO_NOTHING)
    amout = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    #1代表支付宝 2代表微信
    is_type = models.SmallIntegerField(default=0)
    #默认情况未支付，2代表已支付mi
    status = models.SmallIntegerField(default=1)


