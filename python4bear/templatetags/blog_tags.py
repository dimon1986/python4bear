from django import template

register = template.Library()
from ..models import Post

@register.simple_tag
def total_posts():
    """Мощь пользовательских тегов шаблонов заключается в том, что можно обрабатывать любые данные 
    и добавлять их в любой шаблон независимо от выполняемого представления"""
    return Post.objects.filter(status='published').count()

