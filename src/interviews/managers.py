from django.db import models
from django.utils import timezone

from .google_analytics import get_most_read_pages


class InterviewManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(InterviewManager, self).filter(draft=False).filter(publish__lte=timezone.now())

    def latest(self, *args, **kwargs):
        return self.active().order_by('-publish')[:3]

    def most_read(self, *args, **kwargs):
        slugs = get_most_read_pages()
        if slugs:
            return self.active().filter(slug__in=slugs)
        return super(InterviewManager, self).none()
