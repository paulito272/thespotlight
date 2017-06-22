from django.views.generic import DetailView, ListView

from blog.interviewees.models import Interviewee


class IntervieweeListView(ListView):
    model = Interviewee
    context_object_name = 'interviewees'
    queryset = model.objects.all()
    template_name = 'interviewee_list.html'


class IntervieweeDetailView(DetailView):
    model = Interviewee
    context_object_name = 'interviewee'
    template_name = 'interviewee_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
