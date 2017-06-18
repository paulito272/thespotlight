from django.conf.urls import url

from .views import (InterviewListView, InterviewCreateView, InterviewUpdateView,
                    InterviewDetailView, InterviewHomeView)

urlpatterns = [
    url(r'^interviews/$', InterviewListView.as_view(), name='list'),
    url(r'^create/$', InterviewCreateView.as_view(), name='create'),
    url(r'^^(?P<slug>[\w-]+)/edit/$', InterviewUpdateView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)/$', InterviewDetailView.as_view(), name='detail'),
    url(r'^$', InterviewHomeView.as_view(), name='home'),
]
