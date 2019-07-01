from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('<int:news_id>/',views.news_detail,name='news_detail'),
    path('search/',views.search,name='search'),
    path('news_list/',views.news_list,name='news_list'),
    path('public_content/',views.public_content,name='public_content'),
    path('search/',views.search,name='search'),
    path('hot_news/',views.hot_news,name='hot_news'),
    path('more/',views.more,name='more'),




]