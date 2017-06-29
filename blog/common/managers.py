import logging
from datetime import timedelta

from django.db import models
from django.utils import timezone

from blog.common.google_analytics import get_most_read_pages

logger = logging.getLogger('blog')


class CommonManager(models.Manager):
    def active(self, *args, **kwargs):
        return super().filter(draft=False).filter(publish__lte=timezone.now())

    def last_week(self, *args, **kwargs):
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(
            days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        return super().filter(draft=False).filter(publish__gte=monday_of_last_week,
                                                  publish__lt=monday_of_this_week)[:1]

    def most_read(self, *args, **kwargs):
        slugs = get_most_read_pages()
        logger.info(slugs)
        if slugs:
            return self.active().filter(slug__in=slugs).order_by('slug')
        return super().none()
