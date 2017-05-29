from django.views.generic import ListView, DetailView

from .models import Interviewee


class IntervieweeListView(ListView):
    model = Interviewee
    context_object_name = 'interviewees'
    queryset = Interviewee.objects.all()
    template_name = 'interviewee_list.html'


class IntervieweeDetailView(DetailView):
    model = Interviewee
    context_object_name = 'interviewee'
    template_name = 'interviewee_detail.html'

    def get_queryset(self):
        qs = super(IntervieweeDetailView, self).get_queryset()
        print(qs)
        return qs
