from django import template

from blog.categories.models import Category

register = template.Library()


@register.inclusion_tag('navigation.html')
def navigation(selected_id=None):
    return {
        'categories': Category.objects.all(),
        'selected': selected_id,
    }
