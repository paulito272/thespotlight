from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.template import defaultfilters
from django.utils.safestring import mark_safe
from interviewees.models import Interviewee
from markdown_deux import markdown
from unidecode import unidecode

from .managers import InterviewManager
from .utils import get_read_time


def upload_location(instance, filename):
    return '{}/{}/{}'.format('interviews', instance.slug, filename)


class Interview(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    interviewee = models.ForeignKey(Interviewee)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location,
                              width_field='width_field',
                              height_field='height_field')
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Publication Date')
    read_time = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Last Updated')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Creation Date')
    slug = models.SlugField(max_length=255, editable=True, blank=True, null=False, unique=True)

    objects = InterviewManager()

    class Meta:
        ordering = ['-timestamp', '-updated']

    def __str__(self):
        return '{} - {}'.format(self.interviewee, self.title)

    def get_absolute_url(self):
        return reverse('interviews:detail', kwargs={'slug': self.slug})

    def get_markdown(self):
        markdown_text = markdown(self.content)
        return mark_safe(markdown_text)


def create_slug(instance, new_slug=None):
    slug = defaultfilters.slugify(unidecode(instance.title))
    if new_slug is not None:
        slug = new_slug
    qs = Interview.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_interview_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        instance.read_time = get_read_time(html_string)


pre_save.connect(pre_save_interview_receiver, sender=Interview)
