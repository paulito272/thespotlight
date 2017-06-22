import logging

from django.db import models
from django.utils import timezone

logger = logging.getLogger('blog')


class SuggestionManager(models.Manager):
    def active(self, *args, **kwargs):
        return super().filter(draft=False).filter(publish__lte=timezone.now())
