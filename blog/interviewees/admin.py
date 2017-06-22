from django.contrib import admin

from blog.interviewees.models import Interviewee


class IntervieweeModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'occupation']
    search_fields = ['first_name', 'last_name', 'occupation', 'date_of_birth']

    class Meta:
        model = Interviewee


admin.site.register(Interviewee, IntervieweeModelAdmin)
