from django.db import models
# Create your models here.
from django.utils.text import Truncator

from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from versatileimagefield.fields import VersatileImageField, PPOIField

class Topic(models.Model):
    """Название Темы"""
    text = models.CharField(max_length=30, unique=True, )
    description = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text

    def get_comment_count(self):
        return Comment.objects.filter(post__topic=self).count()

    def get_last_comment(self):
        return Comment.objects.filter(post__topic=self).order_by('-date_added').first()

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class TaggedManager(models.Manager):
    def get_query_set(self):
        return super(TaggedManager, self).get_query_set().prefetch_related('tagged_items__tag')

class Post(models.Model):
    """Сам Пост и его поля"""
    STATUS_CHOICES = (
        ('draft', 'Заготовка'),
        ('published', 'Опубликованно'),
    )
    owner = models.ForeignKey(User, related_name='posts', verbose_name='Создатель')

    slug = models.SlugField(max_length=250, unique_for_date='publish') #я так и не разобрался у урами

    topic = models.ForeignKey(Topic, related_name='posts', verbose_name='Тема')
    title = models.CharField(max_length=60, verbose_name='Название')
    text = RichTextUploadingField(blank=True, default='', verbose_name='Содержание')

    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Изменён')

    publish = models.DateTimeField(default=timezone.now, verbose_name='Публикация')
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')

    image = VersatileImageField(upload_to='post_images/',
                                blank=True,
                                ppoi_field='ppoi',
                                verbose_name='ФотоЗпись')

    ppoi = PPOIField(
        'Image PPOI'
    )
    views = models.PositiveIntegerField(default=0)

    objects = models.Manager()  # Менеджер по умолчанию.
    published = PublishedManager()  # Dahl-специальный менеджер.
    tags = TaggableManager(blank=True,)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.title

    def image_img(self):
        if self.image:
            return u'<a href="{0}" target="_blank"><img src="{0}" width="50"/></a>'.format(self.image.url)
        else:
            return '(Нет изображения)'

    image_img.short_description = 'Привьюшка'
    image_img.allow_tags = True

    def get_absolute_url(self):
        return reverse('python4bear:view_post',
                       args=[self.topic.pk,
                             self.slug])

    def get_views_plus(self):
        #я честно скажу не знаю как делается так не так, но так можно, уже знаю, но так всё равно пока лучше.
        self.views += 1
        self.date_added = self.updated
        self.save()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-publish',)


class Comment(models.Model):
    """Комментарии упырей и ко"""
    text = models.TextField(max_length=3000, verbose_name='Коммент')
    post = models.ForeignKey(Post, related_name='comment')
    owner = models.ForeignKey(User, related_name='comment', verbose_name='Знаток')
    owner_up = models.ForeignKey(User, null=True, related_name='+')

    date_added = models.DateTimeField(auto_now_add=True)
    date_up = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        """Возвращает строковое представление модели."""
        truncated_text = Truncator(self.text)
        return truncated_text.chars(30)

    class Meta:
        ordering = ('date_added',)
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'



