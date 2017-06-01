import unicodedata

from django.template import Library

register = Library()


@register.filter
def accentify(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')
