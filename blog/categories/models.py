from django.db import models
from django.db.models.signals import pre_save
from django.template import defaultfilters
from unidecode import unidecode


class Category(models.Model):
    CATEGORY_CHOICES = (
        ('interviews', 'Συντεντεύξεις'),
        ('suggestions', 'Προτάσεις')
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='interviews',
        verbose_name='Category'
    )
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, editable=True, blank=True, null=False, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}: {}'.format(self.get_category_display(), self.name)


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
