from django.utils import timezone
from django.views.generic import DetailView, ListView

from blog.base.mixins import SearchMixin
from blog.categories.models import Category
from blog.interviews.models import Interview


class InterviewListView(SearchMixin, ListView):
    model = Interview
    context_object_name = 'interviews'
    template_name = 'interview_list.html'


class InterviewDetailView(SearchMixin, DetailView):
    model = Interview
    context_object_name = 'interview'
    template_name = 'interview_detail.html'
    today = timezone.now().date()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interview = self.get_object()
        context['title'] = '{}: {}'.format(interview.interviewee, interview.title)
        context['today'] = self.today
        return context


class InterviewCategoryListView(SearchMixin, ListView):
    model = Interview
    context_object_name = 'interviews'
    template_name = 'interview_list.html'
    paginate_by = 10
    page_request_var = 'page'
    context = {
        'page_request_var': page_request_var,
    }

    def get_queryset(self):
        category_slug = self.kwargs['category'] if 'category' in self.kwargs else ''
        category = Category.objects.filter(slug=category_slug)
        return self.model.objects.active().filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in self.context.items():
            context[key] = self.context[key]
        return context
