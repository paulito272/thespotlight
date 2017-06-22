from django import template

from blog.categories.models import Category

register = template.Library()


@register.inclusion_tag('navigation.html')
def navigation():
    return {
        'interviews': Category.objects.filter(category='interviews'),
        'suggestions': Category.objects.filter(category='suggestions')
    }
