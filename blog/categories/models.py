from django.db import models
from django.db.models.signals import pre_save
from django.template import defaultfilters
from unidecode import unidecode


class Category(models.Model):
    position = models.PositiveSmallIntegerField(default=1, blank=False, unique=True)
    name = models.CharField(max_length=120, unique=True)
    sub_categories = models.ManyToManyField('Subcategory', blank=True)
    slug = models.SlugField(max_length=255, editable=True, blank=True, null=False, unique=True)

    class Meta:
        ordering = ['position']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=255, editable=True, blank=True, null=False, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

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


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_receiver, sender=Category)
pre_save.connect(pre_save_receiver, sender=Subcategory)
