from django.conf.urls import url

from blog.suggestions.views import (SuggestionCategoryListView,
                                    SuggestionDetailView, SuggestionListView)

urlpatterns = [
    url(r'^(?P<category>[\w]+)/$', SuggestionCategoryListView.as_view(), name='category'),
    url(r'^(?P<slug>[\w-]+)/$', SuggestionDetailView.as_view(), name='detail'),
    url(r'^$', SuggestionListView.as_view(), name='list'),
]
