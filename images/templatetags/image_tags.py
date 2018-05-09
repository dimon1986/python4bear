from django import template

register = template.Library()
from ..models import Image

@register.simple_tag
def total_image():
    """Мощь пользовательских тегов шаблонов заключается в том, что можно обрабатывать любые данные 
    и добавлять их в любой шаблон независимо от выполняемого представления"""
    return Image.objects.all().count()

