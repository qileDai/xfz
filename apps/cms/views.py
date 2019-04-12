from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from apps.cms.models import NewsCategroy
from utils import restful
from apps.cms.forms import EditNewsCategroyForm, writeNewsForm, addBannersForm, editBannerForm
from apps.news.models import News, Banners
import os
from django.conf import settings
import qiniu
from django.contrib.auth import get_user
from apps.xfzauth.models import User
from apps.news.serializers import BannersSerializers
from datetime import datetime
from django.core.paginator import Paginator
from urllib import parse
from django.utils.timezone import make_aware
from apps.xfzauth.decorator import xfz_login_required


# Create your views here.
@staff_member_required(login_url='index')
def index(request):
    return render(request, "cms/index.html")


def getaroty(request):
    return render(request, "cms/index.html")


def banners(request):
    return render(request, 'cms/banners.html')


class writeNewsView(View):

    def get(self, request):
        categories = NewsCategroy.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/writeNews.html', context=context)

    def post(self, request):
        form = writeNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            categroy_id = form.cleaned_data.get('categroy')
            categroy = NewsCategroy.objects.get(pk=categroy_id)

            News.objects.create(title=title, desc=desc, thumbnail=thumbnail, content=content, categroy=categroy,
                                author=get_user(request))

            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_GET
def news_categroy(request):
    categories = NewsCategroy.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/news_categroy.html', context=context)


@require_POST
def add_news_categroy(request):
    name = request.POST.get('name')
    exists = NewsCategroy.objects.filter(name=name).exists()
    if not exists:
        NewsCategroy.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message="该分类已经存在")


@require_POST
def edit_news_categroy(request):
    form = EditNewsCategroyForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategroy.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message="该新闻分类不存在")
    else:
        return restful.params_error(message=form.get_error())


def delete_news_categroy(request):
    pk = request.POST.get('pk')
    try:
        NewsCategroy.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message="该新闻分类不存在")

class EditNewsView(View):
    def get(self,request):
        news_id = request.POST.get('news_id')
        # print('news_id:'+str(news_id))
        news = News.objects.get(pk=news_id)
        context = {
            'news':news,
            'categories':NewsCategroy.objects.all()
        }
        return render(request,'cms/writeNews.html',context=context)
class NewsListView(View):
    def get(self, request):
        # request.GET：获取出来的所有数据，都是字符串类型
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        # request.GET.get(参数,默认值)
        # 这个默认值是只有这个参数没有传递的时候才会使用
        # 如果传递了，但是是一个空的字符串，那么也不会使用默认值
        category_id = int(request.GET.get('categroy', 0) or 0)

        newses = News.objects.select_related('categroy', 'author')

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2018, month=6, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_tiem__range=(make_aware(start_date), make_aware(end_date)))


        if title:
            newses = newses.filter(title__icontains=title)

        if category_id:
            newses = newses.filter(categroy=category_id)

        paginator = Paginator(newses, 2)
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'categories': NewsCategroy.objects.all(),
            'newses': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }
        context.update(context_data)

        return render(request, 'cms/news_list.html', context=context)



    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
        url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL + name))

        return restful.result(data={'url': url})


@require_GET
def qntoken(request):
    accessKey = settings.QINIU_ACCESS_KEY
    secretKey = settings.QINIU_SECRET_KEY
    bucket = settings.QINIU_BUCKET_NAME
    q = qiniu.Auth(accessKey, secretKey)
    token = q.upload_token(bucket)

    return restful.result(data={'token': token})


def banners_list(request):
    banners = Banners.objects.all()
    serializers = BannersSerializers(banners, many=True)
    return restful.result(data=serializers.data)


def add_banners(request):
    form = addBannersForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        link_to = form.cleaned_data.get('link_to')
        image_url = form.cleaned_data.get('image_url')
        banner = Banners.objects.create(priority=priority, link_to=link_to, image_url=image_url)
        return restful.result(data={'banner_id': banner.pk})
    else:
        return restful.params_error(message=form.get_errors())


def edit_banner(request):
    form = editBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        priority = form.cleaned_data.get('priority')
        link_to = form.cleaned_data.get('link_to')
        image_url = form.cleaned_data.get('image_url')
        Banners.objects.filter(pk=pk).update(priority=priority, link_to=link_to, image_url=image_url)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banners.objects.filter(pk=banner_id).delete()
    return restful.ok()

def delete_newList(request):
    news_id = request.POST.get('news_id')
    News.objects.filter(pk=news_id).delete()
    return restful.ok()

def dasbaord(request):
    return render(request,'base/dashboard.html')

