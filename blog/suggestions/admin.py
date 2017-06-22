from django.contrib import admin

from blog.suggestions.forms import SuggestionModelForm
from blog.suggestions.models import Suggestion


class SuggestionModelAdmin(admin.ModelAdmin):
    form = SuggestionModelForm
    change_form_template = 'admin/change_form.html'
    list_display = ('title', 'publish', 'updated')
    list_filter = ('publish', 'updated', 'timestamp')
    search_fields = ('title', 'content')


admin.site.register(Suggestion, SuggestionModelAdmin)
