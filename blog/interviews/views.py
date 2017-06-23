import logging

from django.db.models import Q
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from blog.categories.models import Category
from blog.interviews.forms import InterviewModelForm
from blog.interviews.models import Interview

logger = logging.getLogger('blog')


class InterviewCreateView(CreateView):
    form_class = InterviewModelForm
    template_name = 'interview_form.html'
    success_url = reverse_lazy('interviews:list')


class InterviewUpdateView(UpdateView):
    form_class = InterviewModelForm
    template_name = 'interview_form.html'

    def get_success_url(self):
        slug = self.kwargs['slug'] if 'slug' in self.kwargs else ''
        return reverse('interviews:detail', kwargs={'slug': slug})


class InterviewListView(ListView):
    model = Interview
    context_object_name = 'interviews'
    template_name = 'interview_list.html'


class InterviewDetailView(DetailView):
    model = Interview
    context_object_name = 'interview'
    template_name = 'interview_detail.html'

    today = timezone.now().date()

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')

        if query:
            query = query.strip()
            queryset = self.model.objects.active().filter(
                Q(title__icontains=query) |
                Q(slug__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(content__icontains=query)
            )
            context = {'interviews': queryset}

            return render(request, 'interview_list_search.html', context)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interview = self.get_object()
        context['title'] = '{}: {}'.format(interview.interviewee, interview.title)
        context['today'] = self.today
        return context


class InterviewCategoryListView(ListView):
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
