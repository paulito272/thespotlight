from django.utils import timezone
from django.views.generic import DetailView, ListView

from blog.base.mixins import ContextMixin, SearchMixin
from blog.base.models import Tag
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
    context = {
        'today': today,
        'dates': model.objects.active().dates('publish', 'month'),
        'tags': Tag.objects.all()
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interview = self.get_object()
        for key, value in self.context.items():
            context[key] = self.context[key]
        context['title'] = '{}: {}'.format(interview.interviewee, interview.title)
        return context


class InterviewDateListView(ContextMixin, SearchMixin, ListView):
    model = Interview
    context_object_name = 'interviews'
    template_name = 'interview_list.html'
    paginate_by = 10
    page_request_var = 'page'
    context = {
        'page_request_var': page_request_var
    }

    def get_queryset(self):
        year = self.kwargs['year'] if 'year' in self.kwargs else ''
        month = self.kwargs['month'] if 'month' in self.kwargs else ''
        return self.model.objects.active().filter(publish__year=year).filter(publish__month=month)


class InterviewTagListView(ContextMixin, SearchMixin, ListView):
    model = Interview
    context_object_name = 'interviews'
    template_name = 'interview_list.html'
    paginate_by = 10
    page_request_var = 'page'
    context = {
        'page_request_var': page_request_var,
    }

    def get_queryset(self):
        tag_slug = self.kwargs['tag'] if 'tag' in self.kwargs else ''
        return self.model.objects.active().filter(tags__slug=tag_slug)


class InterviewCategoryListView(ContextMixin, SearchMixin, ListView):
    model = Interview
    context_object_name = 'interviews'
    template_name = 'interview_list.html'
    paginate_by = 10
    page_request_var = 'page'
    context = {
        'page_request_var': page_request_var
    }

    def get_queryset(self):
        category_slug = self.kwargs['category'] if 'category' in self.kwargs else ''
        category = Category.objects.filter(slug=category_slug)
        return self.model.objects.active().filter(category=category)
