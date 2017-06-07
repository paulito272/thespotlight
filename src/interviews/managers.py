import logging
from datetime import timedelta

from django.db import models
from django.utils import timezone

from .google_analytics import get_most_read_pages

logger = logging.getLogger(__name__)


class InterviewManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(InterviewManager, self).filter(draft=False).filter(publish__lte=timezone.now())

    def newest(self, *args, **kwargs):
        return self.active()[:1]

    def last_week(self, *args, **kwargs):
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        return super(InterviewManager, self).filter(draft=False).filter(publish__gte=monday_of_last_week,
                                                                        publish__lt=monday_of_this_week)[:1]

    def most_read(self, *args, **kwargs):
        queryset = super(InterviewManager, self).none()

        pages = dict(get_most_read_pages())
        if pages:
            interviews = list(self.active().filter(slug__in=list(pages.keys())))
            if (interviews):
                interviews.sort(key=lambda obj: int(pages[obj.slug]), reverse=True)
                ids = [int(obj.id) for obj in interviews]
                clauses = ' '.join(['WHEN id={} THEN {}'.format(pk, i) for i, pk in enumerate(ids)])
                ordering = 'CASE {} END'.format(clauses)
                queryset = super(InterviewManager, self).filter(pk__in=ids).extra(
                    select={'ordering': ordering}, order_by=('ordering',))
                logger.info(queryset)
                return queryset

        return queryset
