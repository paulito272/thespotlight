import unicodedata

from django.template import Library

register = Library()


@register.filter
def accentify(value):
    return ''.join(c for c in unicodedata.normalize('NFD', value)
                   if unicodedata.category(c) != 'Mn')
