from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from unidecode import unidecode


def upload_location(instance, filename):
    return '{}/{}_{}'.format('interviewees', instance.slug, filename)


class Interviewee(models.Model):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    profile_image = models.ImageField(upload_to=upload_location,
                                      width_field='width_field',
                                      height_field='height_field')
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    photographer = models.CharField(_('photographer name'), max_length=90, blank=True, null=True)
    place_of_birth = models.CharField(_('place of birth'), max_length=90, blank=True, null=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    occupation = models.CharField(_('occupation'), max_length=30, blank=True, null=True)
    slug = models.SlugField(max_length=255, editable=True, blank=True, null=False, unique=True)

    class Meta:
        verbose_name = _('interviewee')
        verbose_name_plural = _('interviewees')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_absolute_url(self):
        return reverse('interviewees:detail', kwargs={'slug': self.slug})


def create_slug(instance, new_slug=None):
    slug = defaultfilters.slugify(unidecode(str(instance)))
    if new_slug is not None:
        slug = new_slug
    qs = Interviewee.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Interviewee)
