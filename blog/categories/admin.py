from django.contrib import admin

from blog.categories.models import Category


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    list_display_links = ('name',)
    list_filter = ('category',)
    search_fields = ('name', 'slug')
    ordering = ('category',)

    class Meta:
        model = Category


admin.site.register(Category, CategoryModelAdmin)
