from django.db import models
from django.utils import timezone


class InterviewManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(InterviewManager, self).filter(draft=False).filter(publish__lte=timezone.now())
