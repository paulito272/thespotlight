from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.template import defaultfilters
from django_wysiwyg import clean_html
from unidecode import unidecode

from categories.models import Subcategory
from interviewees.models import Interviewee
from interviews.managers import InterviewManager
from interviews.utils import get_read_time


class Interview(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    interviewee = models.ForeignKey(Interviewee)
    category = models.ForeignKey(Subcategory)
    title = models.CharField(max_length=120)
    content = models.TextField()
    publish = models.DateField(auto_now=False, auto_now_add=False,
                               verbose_name='Publication Date')
    draft = models.BooleanField(default=False)
    read_time = models.IntegerField(default=0, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False,
                                   verbose_name='Last Updated')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True,
                                     verbose_name='Creation Date')
    slug = models.SlugField(max_length=255, editable=True, blank=True, null=False, unique=True)

    objects = InterviewManager()

    class Meta:
        ordering = ['-publish', '-updated', '-timestamp']

    def __str__(self):
        return '{} - {}'.format(self.interviewee, self.title)

    def get_absolute_url(self):
        return reverse('interviews:detail', kwargs={'slug': self.slug})


def create_slug(instance, new_slug=None):
    slug = defaultfilters.slugify(unidecode(instance.interviewee.slug))
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
        instance.read_time = get_read_time(clean_html(instance.content))


pre_save.connect(pre_save_interview_receiver, sender=Interview)
