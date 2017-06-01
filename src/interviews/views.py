import logging

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
        'active_interviews': model.objects.active(),
        'most_read': model.objects.most_read()
    }

    def get_queryset(self):
        queryset = self.model.objects.latest()

        if self.request.GET.get('category'):
            category_slug = self.request.GET.get('category')
            category = Subcategory.objects.filter(slug=category_slug)
            queryset = self.model.objects.filter(category=category)

        return queryset

    def get(self, request, *args, **kwargs):

        # Update every time
        self.context['new_interview'] = self.model.objects.new()
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


class InterviewDetailView(DetailView):
    model = Interview
    context_object_name = 'interview'
    template_name = 'interview_detail.html'

    today = timezone.now().date()

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

# def post_create(request):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#
#     form = PostForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.save()
#         # message success
#         messages.success(request, "Successfully Created")
#         return HttpResponseRedirect(instance.get_absolute_url())
#     context = {
#         "form": form,
#     }
#     return render(request, "interview_form.html", context)


# def post_detail(request, slug=None):
#     instance = get_object_or_404(Post, slug=slug)
#     if instance.publish > timezone.now().date() or instance.draft:
#         if not request.user.is_staff or not request.user.is_superuser:
#             raise Http404
#     share_string = quote_plus(instance.content)
#
#     initial_data = {
#         "content_type": instance.get_content_type,
#         "object_id": instance.id
#     }
#     form = CommentForm(request.POST or None, initial=initial_data)
#     if form.is_valid() and request.user.is_authenticated():
#         c_type = form.cleaned_data.get("content_type")
#         content_type = ContentType.objects.get(model=c_type)
#         obj_id = form.cleaned_data.get('object_id')
#         content_data = form.cleaned_data.get("content")
#         parent_obj = None
#         try:
#             parent_id = int(request.POST.get("parent_id"))
#         except:
#             parent_id = None
#
#         if parent_id:
#             parent_qs = Comment.objects.filter(id=parent_id)
#             if parent_qs.exists() and parent_qs.count() == 1:
#                 parent_obj = parent_qs.first()
#
#         new_comment, created = Comment.objects.get_or_create(
#             user=request.user,
#             content_type=content_type,
#             object_id=obj_id,
#             content=content_data,
#             parent=parent_obj,
#         )
#         return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
#
#     comments = instance.comments
#     context = {
#         "title": instance.title,
#         "instance": instance,
#         "share_string": share_string,
#         "comments": comments,
#         "comment_form": form,
#     }
#     return render(request, "interview_detail.html", context)



# def post_update(request, slug=None):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#     instance = get_object_or_404(Post, slug=slug)
#     form = PostForm(request.POST or None, request.FILES or None, instance=instance)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
#         return HttpResponseRedirect(instance.get_absolute_url())
#
#     context = {
#         "title": instance.title,
#         "instance": instance,
#         "form": form,
#     }
#     return render(request, "interview_form.html", context)
#
#
# def post_delete(request, slug=None):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#     instance = get_object_or_404(Post, slug=slug)
#     instance.delete()
#     messages.success(request, "Successfully deleted")
#     return redirect("interviews:list")
