from django.conf.urls import url

from interviewees.views import IntervieweeListView, IntervieweeDetailView

urlpatterns = [
    url(r'^$', IntervieweeListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', IntervieweeDetailView.as_view(), name='detail'),
]
