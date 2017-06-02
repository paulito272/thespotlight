import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView

from categories.models import Subcategory
from .forms import InterviewModelForm
from .models import Interview

logger = logging.getLogger(__name__)


class InterviewCreateView(CreateView):
    form_class = InterviewModelForm
    template_name = 'interview_form.html'
    success_url = reverse_lazy('interviews:list')


class InterviewListView(ListView):
    model = Interview
    context_object_name = 'interviews'
    template_name = 'interview_list.html'
    paginate_by = 10

    today = timezone.now().date()
    page_request_var = 'page'
    context = {
        'today': today,
        'page_request_var': page_request_var,
        'new_interview': model.objects.new(),
        'most_read': model.objects.most_read(),
        'last_week_interview': model.objects.last_week(),
        'active_interviews': model.objects.active()
    }

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        category_slug = request.GET.get('category')

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

        if category_slug:
            category_slug = category_slug.strip()
            category = get_object_or_404(Subcategory, slug=category_slug)

            queryset = self.model.objects.active().filter(category=category)
            context = {'category': category, 'interviews': queryset}

            return render(request, 'interview_list_category.html', context)

        # Update every time
        self.context['new_interview'] = self.model.objects.new()
        self.context['last_week_interview'] = self.model.objects.last_week()
        self.context['active_interviews'] = self.model.objects.active()

        # Update every day
        days_past = (timezone.now().date() - self.context['today']).days
        if (days_past >= 1):
            self.context['most_read'] = self.model.objects.most_read()

        return super(InterviewListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InterviewListView, self).get_context_data(**kwargs)
        for key, value in self.context.items():
            context[key] = self.context[key]
        return context

    def get_queryset(self):
        # Get the last 9 interviews
        return self.model.objects.active().order_by('-publish')[:9]


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

        return super(InterviewDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InterviewDetailView, self).get_context_data(**kwargs)
        interview = self.get_object()
        context['title'] = '{}: {}'.format(interview.interviewee, interview.title)
        context['today'] = self.today
        return context


class InterviewUpdateView(UpdateView):
    form_class = InterviewModelForm
    model = Interview
    template_name = 'interview_form.html'

    def get_success_url(self):
        slug = self.kwargs['slug'] if 'slug' in self.kwargs else ''
        return reverse('interviews:detail', kwargs={'slug': slug})
