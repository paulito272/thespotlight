from django.conf.urls import url

from blog.interviews.views import InterviewTagListView, InterviewCategoryListView, InterviewDetailView, InterviewListView

urlpatterns = [
    url(r'^tag/(?P<tag>[\w]+)/$', InterviewTagListView.as_view(), name='tag'),
    url(r'^category/(?P<category>[\w]+)/$', InterviewCategoryListView.as_view(), name='category'),
    url(r'^(?P<slug>[\w-]+)/$', InterviewDetailView.as_view(), name='detail'),
    url(r'^$', InterviewListView.as_view(), name='list'),
]
