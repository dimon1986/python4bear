from django.db import models
from django.utils.html import mark_safe
from markdown import markdown

# Create your models here.
from django.utils.text import Truncator
import math
from django.contrib.auth.models import User


# Create your models here.

class Topic(models.Model):
    """Название Темы"""
    text = models.CharField(max_length=30, unique=True, )
    description = models.CharField(max_length=120)
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


class Post(models.Model):
    """Сам Пост и его поля"""
    owner = models.ForeignKey(User, related_name='posts', verbose_name='Создатель')
    topic = models.ForeignKey(Topic, related_name='posts', verbose_name='Тема')
    title = models.CharField(max_length=60, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/',
                              blank=True, verbose_name='ФотоЗпись')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        """Возвращает строковое представление модели."""
        if len(self.text) > 100:
            return self.text[:100] + "..."
        return self.text

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    """Комментарии упырей и ко"""
    text = models.TextField(max_length=3000, verbose_name='Коммент')
    post = models.ForeignKey(Post, related_name='comment')
    owner = models.ForeignKey(User, related_name='comment', verbose_name='Знаток')
    owner_up = models.ForeignKey(User, null=True, related_name='+')
    date_added = models.DateTimeField(auto_now_add=True)
    date_up = models.DateTimeField(null=True)

    def __str__(self):
        """Возвращает строковое представление модели."""
        truncated_text = Truncator(self.text)
        return truncated_text.chars(30)

    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.text, safe_mode='escape'))



