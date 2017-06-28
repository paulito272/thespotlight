from django.conf.urls import url

from blog.interviews.views import InterviewCategoryListView, InterviewDetailView, InterviewListView

urlpatterns = [
    url(r'^category/(?P<category>[\w]+)/$', InterviewCategoryListView.as_view(), name='category'),
    url(r'^(?P<slug>[\w-]+)/$', InterviewDetailView.as_view(), name='detail'),
    url(r'^$', InterviewListView.as_view(), name='list'),
]
