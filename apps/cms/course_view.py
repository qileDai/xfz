#encoding:utf-8
from apps.news.models import News
from .models import NewsCategroy
from django.shortcuts import render
from utils import restful
from .forms import pubCourseForm
from apps.course.models import Course,Teacher,CourseCategroy
from django.views.generic import View


class pubCourse(View):
    def get(self,request):
        context = {
            'categroies':CourseCategroy.objects.all(),
            'teachers':Teacher.objects.all()
        }
        return render(request,'cms/pub_course.html',context=context)

    def post(self,request):
        form = pubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            categroy_id = form.cleaned_data.get('categroy')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher')

            categroy = CourseCategroy.objects.get(pk=categroy_id)
            print(categroy)
            teacher = Teacher.objects.get(pk=teacher_id)
            print(teacher)

            Course.objects.create(title=title,video_url=video_url,cover_url=cover_url,price=price,
                                  duration=duration,profile=profile,categroy=categroy,teacher=teacher)
            return restful.ok()
        else:
            return restful.params_error(form.get_errors())




