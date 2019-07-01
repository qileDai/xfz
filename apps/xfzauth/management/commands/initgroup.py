#encoding=utf-8

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission,ContentType
from apps.news.models import News,Banners,Comment
from apps.cms.models import NewsCategroy
from apps.course.models import CourseOrder,Course,CourseCategroy,Teacher

class Command(BaseCommand):
    def handle(self, *args, **options):
        #1、编辑组（管理文章/管理课程/管理评论/管理轮播图）
        edit_conten_type = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(Banners),
            ContentType.objects.get_for_model(NewsCategroy),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategroy),
            ContentType.objects.get_for_model(Teacher),
        ]
        edit_permission = Permission.objects.filter(content_type__in=edit_conten_type)
        editGroup = Group.objects.create(name='编辑')
        editGroup.permissions.set(edit_permission)
        editGroup.save()
        self.stdout.write(self.style.SUCCESS("编辑组创建成功"))

        #2、财务组（课程订单/付费）
        finance_content_type =[
            ContentType.objects.get_for_model(CourseOrder),
        ]
        finance_permission = Permission.objects.filter(content_type__in=finance_content_type)
        financeGroup = Group.objects.create(name='财务')
        financeGroup.permissions.set(finance_permission)
        financeGroup.save()
        self.stdout.write(self.style.SUCCESS("财务组创建成功"))

        #3、管理员组（编辑组+财务组）
        admin_permission  = edit_permission.union(finance_permission)
        adminGroup = Group.objects.create(name='管理员')
        adminGroup.permissions.set(admin_permission)
        adminGroup.save()
        self.stdout.write(self.style.SUCCESS("管理员组创建成功"))
        #4、超级管理员
