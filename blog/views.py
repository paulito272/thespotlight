from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.utils import timezone
from django.views.generic import FormView, ListView

from blog.forms import ContactForm
from blog.interviews.models import Interview
from blog.suggestions.models import Suggestion


class HomeView(ListView):
    model = Interview
    queryset = model.objects.active()
    context_object_name = 'interviews'
    template_name = 'home.html'
    page_request_var = 'page'
    paginate_by = 10

    today = timezone.now().date()
    context = {
        'today': today,
        'page_request_var': page_request_var,
        'most_read_interviews': model.objects.most_read(),
        'last_week_interview': model.objects.last_week(),
        'active_interviews': model.objects.active(),
        'suggestions': Suggestion.objects.active()
    }

    def get(self, request, *args, **kwargs):
        # Update every time
        self.context['last_week_interview'] = self.model.objects.last_week()
        self.context['active_interviews'] = self.model.objects.active()

        # Update every day
        days_past = (timezone.now().date() - self.context['today']).days
        if days_past >= 1:
            self.context['most_read_interviews'] = self.model.objects.most_read()

        return super().get(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     query = request.GET.get('q')
    #
    #     if query:
    #         query = query.strip()
    #         queryset = self.model.objects.active().filter(
    #             Q(title__icontains=query) |
    #             Q(slug__icontains=query) |
    #             Q(author__first_name__icontains=query) |
    #             Q(author__last_name__icontains=query) |
    #             Q(content__icontains=query)
    #         )
    #         context = {'interviews': queryset}
    #
    #         return render(request, 'interview_list_search.html', context)
    #
    #     return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in self.context.items():
            context[key] = self.context[key]
        return context


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = '/contact/'

    def form_valid(self, form):
        message = '{name} ({email}): '.format(name=form.cleaned_data.get('name'),
                                              email=form.cleaned_data.get('email'))
        message += '\n\n{0}'.format(form.cleaned_data.get('message'))

        mail_admins(
            subject=form.cleaned_data.get('subject').strip(),
            message=message,
            fail_silently=True
        )

        send_mail(
            subject='Σας ευχαριστούμε για το μήνυμά σας.',
            message='Ευχαριστούμε!\n'
                    'Το μήνυμά σας έχει σταλεί με επιτυχία.\n'
                    'Θα επικοινωνούσουμε μαζί σας το συντομότερο δυνατό.\n\n'
                    'Με εκτίμηση,\n'
                    'Η ομάδα του thespotlight.gr',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[form.cleaned_data.get('email')],
            fail_silently=True
        )

        return super().form_valid(form)
