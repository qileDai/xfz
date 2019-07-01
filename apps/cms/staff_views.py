
#encoding=utf-8

from django.shortcuts import render,redirect,reverse
from apps.xfzauth.models import User
from django.views.generic import View
from django.contrib.auth.models import Group
from utils import restful

def staffs_view(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs':staffs
    }

    return render(request,'cms/staff.html',context=context)


class AddStaffsView(View):
    def get(self,request):
        groups = Group.objects.all()
        context = {
            'groups': groups

        }
        return render(request,'cms/add_staffs.html',context=context)
    def post(self,request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        user.is_staff = True
        group_ids = request.POST.getlist('groups')
        print(group_ids)
        groups = Group.objects.filter(pk__in=group_ids)
        user.groups.set(groups)
        print(user)
        user.save()

        return redirect(reverse('cms:staffs'))


def delete_staffs(request):
    telephone = request.POST.get('telephone')
    User.objects.filter(telephone=telephone).delete()
    return restful.ok()



