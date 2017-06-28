from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from django_wysiwyg import clean_html
from unidecode import unidecode

from blog.categories.models import Category
from blog.interviews.utils import get_read_time
from blog.suggestions.managers import SuggestionManager


def upload_location(instance, filename):
    return '{}/{}_{}'.format('suggestions', instance.slug, filename)


class Suggestion(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=120)
    content = models.TextField()
    tags = models.ManyToManyField('base.Tag', related_name='suggestions')
    publish = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Publication Date')
    draft = models.BooleanField(default=False)
    read_time = models.IntegerField(default=0, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Last Updated')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True,
                                     verbose_name='Creation Date')
    image = models.ImageField(upload_to=upload_location, width_field='width_field',
                              height_field='height_field')
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    photographer = models.CharField(_('photographer name'), max_length=90, blank=True, null=True)
    slug = models.SlugField(max_length=255, editable=True, blank=True, null=False, unique=True)

    objects = SuggestionManager()

    class Meta:
        ordering = ['-publish', '-updated', '-timestamp']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('suggestions:detail', kwargs={'slug': self.slug})


def create_slug(instance, new_slug=None):
    slug = defaultfilters.slugify(unidecode(instance.slug))
    if new_slug is not None:
        slug = new_slug
    qs = Suggestion.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_suggestion_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        instance.read_time = get_read_time(clean_html(instance.content))


pre_save.connect(pre_save_suggestion_receiver, sender=Suggestion)
