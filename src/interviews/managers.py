from datetime import timedelta

from django.db import models
from django.utils import timezone

from .google_analytics import get_most_read_pages


class InterviewManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(InterviewManager, self).filter(draft=False).filter(publish__lte=timezone.now())

    def new(self, *args, **kwargs):
        return self.active().first()

    def last_week(self, *args, **kwargs):
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        return super(InterviewManager, self).filter(draft=False).filter(publish__gte=monday_of_last_week,
                                                                        publish__lt=monday_of_this_week)[:1]

    def most_read(self, *args, **kwargs):
        pages = dict(get_most_read_pages())

        if pages:
            objects = list(self.active().filter(slug__in=pages))
            objects.sort(key=lambda obj: pages[obj.slug])
            return objects

        return super(InterviewManager, self).none()
