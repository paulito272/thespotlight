from django.contrib import admin

from .models import Interview


class InterviewModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated']
    list_filter = ['updated', 'timestamp']
    search_fields = ['title', 'content', 'interviewee']

    class Meta:
        model = Interview


admin.site.register(Interview, InterviewModelAdmin)
