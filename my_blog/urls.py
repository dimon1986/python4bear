"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.sitemaps.views import sitemap
from python4bear.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'', include('python4bear.urls', namespace='python4bear')),
    url(r'', include('accounts.urls', namespace='accounts')),
    url(r'', include('search.urls', namespace='search')),
    url(r'^images/', include('images.urls', namespace='images')),
    url(r'^polls/', include('polls.urls', namespace='polls')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url('^', include('django.contrib.auth.urls')),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
