from django.conf.urls import url
from . import views

urlpatterns = [
    # создание картинки для сайта спомощю джаваскрипта
    url(r'^create/$', views.image_create, name='create'),
    # детали картинки если слунга не будет будет ошибка!!
    url(r'^detail/(?P<slug>[-\w]+)/$', views.image_detail, name='detail'),
    url(r'^like/$', views.image_like, name='like'),
    #url(r'^ranking/$', views.image_ranking, name='create'),
    # поидее все картинки с панигацией, но посмотрим
    url(r'^$', views.image_list, name='list'),
]