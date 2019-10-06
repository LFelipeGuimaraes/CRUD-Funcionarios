import datetime
from django import template

register = template.Library()

@register.simple_tag
def hora_atual():
    return datetime.datetime.now().strftime('%H:%M:%S')