from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from blog.suggestions.models import Suggestion


class SuggestionListView(ListView):
    model = Suggestion
    queryset = model.objects.all()
    context_object_name = 'suggestions'
    template_name = 'suggestion_list.html'
    paginate_by = 10

    today = timezone.now().date()
    page_request_var = 'page'
    context = {
        'today': today,
        'page_request_var': page_request_var,
    }

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        suggestion_slug = request.GET.get('category')

        if query:
            query = query.strip()
            queryset = self.model.objects.active().filter(
                Q(title__icontains=query) |
                Q(slug__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(content__icontains=query)
            )
            context = {'suggestions': queryset}

            return render(request, 'suggestion_list_search.html', context)

        if suggestion_slug:
            suggestion_slug = suggestion_slug.strip()
            category = get_object_or_404(Suggestion, slug=suggestion_slug)

            queryset = self.model.objects.active().filter(category=category)
            context = {'category': category, 'suggestions': queryset}

            return render(request, 'suggestion_list_search.html', context)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in self.context.items():
            context[key] = self.context[key]
        return context


class SuggestionCategoryListView(ListView):
    model = Suggestion
    context_object_name = 'suggestions'
    template_name = 'suggestion_list.html'
    paginate_by = 10

    today = timezone.now().date()
    page_request_var = 'page'
    context = {
        'today': today,
        'page_request_var': page_request_var,
    }

    def get_queryset(self):
        return self.model.objects.active(category=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in self.context.items():
            context[key] = self.context[key]
        return context


class SuggestionDetailView(DetailView):
    model = Suggestion
    context_object_name = 'suggestion'
    template_name = 'suggestion_detail.html'

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
            context = {'suggestions': queryset}

            return render(request, 'suggestion_list_search.html', context)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suggestion = self.get_object()
        context['title'] = suggestion.title
        context['today'] = self.today
        return context
