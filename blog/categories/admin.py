from django.contrib import admin

from blog.categories.models import Category, Subcategory

admin.site.register(Category)
admin.site.register(Subcategory)
