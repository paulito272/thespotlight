from django.db import models
from django.db.models.signals import pre_save
from django.template import defaultfilters
from unidecode import unidecode


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=255, editable=True, blank=True, null=False, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


def create_slug(instance, new_slug=None):
    slug = defaultfilters.slugify(unidecode(instance.name))
    if new_slug is not None:
        slug = new_slug
    qs = Category.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_interview_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_interview_receiver, sender=Category)
