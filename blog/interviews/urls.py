from django.conf.urls import url

from blog.interviews.views import (InterviewCategoryListView, InterviewCreateView,
                                   InterviewDetailView, InterviewListView, InterviewUpdateView)

urlpatterns = [
    url(r'^category/(?P<category>[\w]+)/$', InterviewCategoryListView.as_view(), name='category'),
    url(r'^create/$', InterviewCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/edit/$', InterviewUpdateView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)/$', InterviewDetailView.as_view(), name='detail'),
    url(r'^$', InterviewListView.as_view(), name='list'),
]
