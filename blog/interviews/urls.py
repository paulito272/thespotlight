from django.conf.urls import url

from blog.interviews.views import (InterviewCategoryListView, InterviewDateListView,
                                   InterviewDetailView, InterviewListView)

urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', InterviewDateListView.as_view(), name='date'),
    url(r'^category/(?P<category>[\w]+)/$', InterviewCategoryListView.as_view(), name='category'),
    url(r'^(?P<slug>[\w-]+)/$', InterviewDetailView.as_view(), name='detail'),
    url(r'^$', InterviewListView.as_view(), name='list'),
]
