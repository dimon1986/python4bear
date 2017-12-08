from django.conf.urls import url
from . import views

urlpatterns = [
    #начальная страница - все темы
    url(r'^$', views.TopicListView.as_view(), name='home'),

    # подробно тема, и список постов
    url(r'^posts_all/(?P<pk>\d+)/$', views.PostsAllListView.as_view(), name='posts_all'),

    # подробно пост и коменты
    url(r'^topic/(?P<pk>\d+)/view_post/(?P<post_pk>\d+)/$', views.view_post, name='view_post'),

    # добавление поста
    url(r'^post/(?P<pk>\d+)/new/$', views.new_post, name='new_post'),

    # редактирование темы хозяином темы
    url(r'^topic/(?P<pk>\d+)/edit_post/(?P<post_pk>\d+)/$', views.PostEditView.as_view(), name='edit_post'),

]