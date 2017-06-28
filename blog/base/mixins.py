from django.db.models import Q
from django.shortcuts import render

from blog.interviews.models import Interview
from blog.suggestions.models import Suggestion


class SearchMixin:
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')

        if query and query.strip():
            interviews_qs = Interview.objects.active().filter(
                Q(title__icontains=query) |
                Q(slug__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(content__icontains=query)
            )
            suggestions_qs = Suggestion.objects.active().filter(
                Q(title__icontains=query) |
                Q(slug__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(content__icontains=query)
            )
            context = {'interviews': interviews_qs, 'suggestions': suggestions_qs}
            return render(request, 'search.html', context)

        return super().get(request, *args, **kwargs)
