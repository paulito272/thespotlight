from django.conf.urls import url

from blog.interviewees.views import IntervieweeDetailView, IntervieweeListView

urlpatterns = [
    url(r'^$', IntervieweeListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', IntervieweeDetailView.as_view(), name='detail'),
]
