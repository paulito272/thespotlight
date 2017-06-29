from django.utils import timezone
from django.views.generic import DetailView, ListView

from blog.base.mixins import ContextMixin, SearchMixin
from blog.base.models import Tag
from blog.categories.models import Category
from blog.suggestions.models import Suggestion


class SuggestionListView(SearchMixin, ListView):
    model = Suggestion
    queryset = model.objects.all()
    context_object_name = 'suggestions'
    template_name = 'suggestion_list.html'


class SuggestionDetailView(SearchMixin, DetailView):
    model = Suggestion
    context_object_name = 'suggestion'
    template_name = 'suggestion_detail.html'
    today = timezone.now().date()
    context = {
        'today': today,
        'suggestions': model.objects.active(),
        'tags': Tag.objects.all()
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suggestion = self.get_object()
        for key, value in self.context.items():
            context[key] = self.context[key]
        context['title'] = suggestion.title
        return context


class SuggestionDateListView(ContextMixin, SearchMixin, ListView):
    model = Suggestion
    context_object_name = 'suggestions'
    template_name = 'suggestion_list.html'
    paginate_by = 10
    page_request_var = 'page'
    context = {
        'page_request_var': page_request_var
    }

    def get_queryset(self):
        year = self.kwargs['year'] if 'year' in self.kwargs else ''
        month = self.kwargs['month'] if 'month' in self.kwargs else ''
        return self.model.objects.active().filter(publish__year=year).filter(publish__month=month)


class SuggestionTagListView(ContextMixin, SearchMixin, ListView):
    model = Suggestion
    context_object_name = 'suggestions'
    template_name = 'suggestion_list.html'
    paginate_by = 10
    page_request_var = 'page'
    context = {
        'page_request_var': page_request_var,
    }

    def get_queryset(self):
        tag_slug = self.kwargs['tag'] if 'tag' in self.kwargs else ''
        return self.model.objects.active().filter(tags__slug=tag_slug)


class SuggestionCategoryListView(ContextMixin, SearchMixin, ListView):
    model = Suggestion
    context_object_name = 'suggestions'
    template_name = 'suggestion_list.html'
    paginate_by = 10
    page_request_var = 'page'
    context = {
        'page_request_var': page_request_var,
    }

    def get_queryset(self):
        category_slug = self.kwargs['category'] if 'category' in self.kwargs else ''
        category = Category.objects.filter(slug=category_slug)
        return self.model.objects.active().filter(category=category)
