from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from blog.interviews.views import InterviewHomeView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^interviews/', include('blog.interviews.urls', namespace='interviews')),
    url(r'^suggestions/', include('blog.suggestions.urls', namespace='suggestions')),
    url(r'^interviewees/', include('blog.interviewees.urls', namespace='interviewees')),
    url(r'^$', InterviewHomeView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)