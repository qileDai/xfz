from django.shortcuts import render
from apps.news.models import News, Banners
from apps.cms.models import NewsCategroy
from django.conf import settings
from .serializers import NewsSerializers, CommentSerializers
from utils import restful
from django.http import Http404
from .forms import publicCommentForm
from .models import Comment
from django.contrib.auth import get_user
from apps.xfzauth.decorator import xfz_login_required
from django.db.models import Q
from django.shortcuts import reverse,redirect
from django.http import HttpResponse


# Create your views here.


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newes = News.objects.all().order_by('-pub_tiem')[0:count]
    categroies = NewsCategroy.objects.all()
    context = {
        'newes': newes,
        'categroies': categroies,
        'banners': Banners.objects.all()
    }
    return render(request, 'news/index.html', context=context)


def news_lists(request):
    # 通过p参数来获取页数
    page = int(request.GET.get('p', 1))
    print(page)
    categroy_id = int(request.GET.get('categroy_id', 0))
    # print(categroy_id)
    newesaa = News.objects.all().order_by('-pub_tiem')

    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    newes = News.objects.all().order_by('-pub_tiem')[start:end]
    serializers = NewsSerializers(newes, many=True)
    data = serializers.data
    print(data)

    return restful.result(data=data)


def news_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    page = int(request.GET.get('p', 1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    categroy_id = int(request.GET.get('categroy_id', 0))
    # 0,1
    # 2,3
    # 4,5
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if categroy_id == 0:
        # QuerySet
        # {'id':1,'title':'abc',category:{"id":1,'name':'热点'}}
        newses = News.objects.select_related('categroy', 'author').all()[start:end]
    else:
        newses = News.objects.select_related('categroy', 'author').filter(categroy_id=categroy_id)[start:end]
        print(categroy_id)
    serializer = NewsSerializers(newses, many=True)
    data = serializer.data
    return restful.result(data=data)


def news_detail(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
        print(news)
        context = {
            'news': news
        }
        print(context)
        return render(request, "news/news_detail.html", context=context)
    except News.DoesNotExist:
        raise Http404


def search(request):
    return render(request, "search/search.html")

@xfz_login_required
def public_content(request):
    forms = publicCommentForm(request.POST)
    if forms.is_valid():
        news_id = forms.cleaned_data.get('news_id')
        content = forms.cleaned_data.get('content')
        if content=='':
            return restful.params_error()
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(news=news, content=content, author=get_user(request))
        serializers = CommentSerializers(comment)

        return restful.result(data=serializers.data)

    else:
        return restful.params_error(forms.get_errors())


def search(request):
    q = request.GET.get('q')
    context = {}
    newses = News.objects.all().order_by('-pub_tiem')[0:5]
    context['newses'] = newses
    if q:
        newses = News.objects.filter(Q(title__icontains=q) | Q(content__contains=q))
        context['newses' ] = newses
    return  render(request,'search/search.html',context=context)


def hot_news(request):
    newes = News.objects.all().order_by('-pub_tiem')[0:5]
    context = {
        'newes':newes
    }
    return render(request,'comment/siderbar.html',context=context)

def more(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newes = News.objects.all().order_by('-pub_tiem')[0:count]
    context = {
       'newes':newes
    }
    return render(request,'news/more.html',context=context)

