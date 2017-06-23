import re

from django.template import Library

register = Library()


@register.filter
def remove_tags(content):
    return re.sub(r'<img.*?/>|<iframe.*?>.*?<\/iframe>', '', content)
