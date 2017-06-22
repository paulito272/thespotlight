import re

from django.template import Library

register = Library()


@register.filter
def remove_img_tags(value):
    p = re.compile(r'<p><img.*?/></p>')
    return p.sub('', value)
