from django.conf.urls import url

from blog.suggestions.views import (SuggestionCategoryListView, SuggestionDateListView,
                                    SuggestionDetailView, SuggestionListView)

urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', SuggestionDateListView.as_view(), name='date'),
    url(r'^category/(?P<category>[\w]+)/$', SuggestionCategoryListView.as_view(), name='category'),
    url(r'^(?P<slug>[\w-]+)/$', SuggestionDetailView.as_view(), name='detail'),
    url(r'^$', SuggestionListView.as_view(), name='list'),
]
