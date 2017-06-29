from django.db import models
from django.db.models.signals import pre_save
from django.template import defaultfilters
from unidecode import unidecode


class Tag(models.Model):
    word = models.CharField(max_length=120)
    slug = models.CharField(max_length=255, editable=True, blank=True, null=False, unique=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.word


def create_slug(instance, new_slug=None):
    slug = defaultfilters.slugify(unidecode(instance.word))
    if new_slug is not None:
        slug = new_slug
    qs = Tag.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_tag_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_tag_receiver, sender=Tag)
