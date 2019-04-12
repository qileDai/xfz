#encoding: utf-8

from django.urls import path
from . import views
from . import course_view as cviews


app_name = 'cms'

urlpatterns = [
    path('index',views.index,name='index'),
    path('',views.getaroty,name='getaroty'),
    path('write_news/',views.writeNewsView.as_view(),name='write_news'),
    path('news_categroy/',views.news_categroy,name='news_categroy'),
    path('add_news_categroy/',views.add_news_categroy,name='add_news_categroy'),
    path('edit_news_categroy/',views.edit_news_categroy,name='edit_news_categroy'),
    path('delete_news_categroy/',views.delete_news_categroy,name='delete_news_categroy'),
    path('banners/',views.banners,name='banners'),
    path('upload_file/',views.upload_file,name='upload_file'),
    path('qntoken/',views.qntoken,name='qntoken'),
    path('add_banners/',views.add_banners,name='add_banners'),
    path('banners_list/',views.banners_list,name='banners_list'),
    path('delete_banner/',views.delete_banner,name='delete_banner'),
    path('edit_banner/',views.edit_banner,name='edit_banner'),
    path('news_list/',views.NewsListView.as_view(),name='news_list'),
    path('news_list/',views.NewsListView.as_view(),name='news_list'),
    path('edit_news/',views.EditNewsView.as_view(),name='edit_news'),
    path('dasbaord/',views.dasbaord,name='dasbaord'),


]

urlpatterns +=[
    path('pubcourse/',cviews.pubCourse.as_view(),name='pubcourse'),

]

