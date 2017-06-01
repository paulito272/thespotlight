import logging

from django.db import models
from django.utils import timezone

from .google_analytics import get_most_read_pages

logger = logging.getLogger(__name__)


class InterviewManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(InterviewManager, self).filter(draft=False).filter(publish__lte=timezone.now())

    def latest(self, *args, **kwargs):
        return self.active().order_by('-publish')[:9]

    def new(self, *args, **kwargs):
        return self.active().first()

    def most_read(self, *args, **kwargs):
        pages = dict(get_most_read_pages())

        if pages:
            objects = list(self.active().filter(slug__in=pages))
            objects.sort(key=lambda obj: pages[obj.slug])
            logger.info('Most read interviews: {}'.format(objects))
            return objects

        return super(InterviewManager, self).none()
