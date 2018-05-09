from django.conf.urls import url
from . import views

from .feeds import LatestPostsFeed

urlpatterns = [
    #привет страница
    url(r'^hell/$', views.hell, name='hell'),

    #основаная страница - все темы
    url(r'^$', views.home, name='home'),

    # подробно тема, и список постов
    url(r'^posts_all/(?P<pk>\d+)/$', views.posts_all, name='posts_all'),
    url(r'^tag/(?P<pk>\d+)/(?P<tag_slug>[-\w]+)/$', views.posts_all, name='post_all_by_tag'),

    # подробно пост и коменты
    url(r'^topic/(?P<pk>\d+)/view_post/'\
        r'(?P<post_name>[-\w]+)/$', views.view_post, name='view_post'),

    # добавление поста
    url(r'^post/(?P<pk>\d+)/new/$', views.new_post, name='new_post'),

    # редактирование темы хозяином темы
    url(r'^topic/(?P<pk>\d+)/edit_post/'\
        r'(?P<post_name>[-\w]+)/$', views.edit_post, name='edit_post'),

    #поделиться сообщением
    url(r'^(?P<post_name>[-\w]+)/share/$', views.post_share, name='post_share'),

    #канал RSS нафиг он только нужен не знаю
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),

]