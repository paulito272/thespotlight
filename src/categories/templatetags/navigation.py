from django import template

from categories.models import Category

register = template.Library()


@register.inclusion_tag('navigation.html')
def navigation(selected_id=None):
    return {
        'categories': Category.objects.all().order_by('-id'),
        'selected': selected_id,
    }
