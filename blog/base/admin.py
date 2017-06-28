from django.contrib import admin

from blog.base.models import Tag


class TagModelAdmin(admin.ModelAdmin):
    list_display = ('word',)
    search_fields = ('word', 'slug')

    class Meta:
        model = Tag


admin.site.register(Tag, TagModelAdmin)
