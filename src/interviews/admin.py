from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from .models import Interview


class InterviewModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    list_display = ['title', 'publish', 'updated']
    list_filter = ['publish', 'updated', 'timestamp']
    search_fields = ['title', 'content', 'interviewee']

    class Meta:
        model = Interview


admin.site.register(Interview, InterviewModelAdmin)
