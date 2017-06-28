from django.contrib import admin

from blog.interviews.forms import InterviewModelForm
from blog.interviews.models import Interview, Tag


class TagModelAdmin(admin.ModelAdmin):
    list_display = ('word',)
    search_fields = ('word', 'slug')

    class Meta:
        model = Tag


admin.site.register(Tag, TagModelAdmin)


class InterviewModelAdmin(admin.ModelAdmin):
    form = InterviewModelForm
    change_form_template = 'admin/change_form.html'
    list_display = ('interviewee', 'title', 'publish', 'updated')
    list_filter = ('publish', 'updated', 'timestamp', 'tags')
    search_fields = ('title', 'content', 'interviewee', 'tags')


admin.site.register(Interview, InterviewModelAdmin)
