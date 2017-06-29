from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.utils import timezone
from django.views.generic import FormView, TemplateView

from blog.base.forms import ContactForm
from blog.base.mixins import ContextMixin, SearchMixin
from blog.interviews.models import Interview
from blog.suggestions.models import Suggestion


class HomeView(ContextMixin, SearchMixin, TemplateView):
    template_name = 'home.html'
    paginate_by = 10
    page_request_var = 'page'
    today = timezone.now().date()
    context = {
        'today': today,
        'page_request_var': page_request_var,
        'most_read_interviews': Interview.objects.most_read(),
        'most_read_suggestions': Suggestion.objects.most_read()
    }

    def get(self, request, *args, **kwargs):
        # Update every time
        self.context['interviews'] = Interview.objects.active()
        self.context['last_week_interview'] = Interview.objects.last_week()

        self.context['suggestions'] = Suggestion.objects.active()
        self.context['last_week_suggestion'] = Suggestion.objects.last_week()

        # Update every day
        days_past = (timezone.now().date() - self.context['today']).days
        if days_past >= 1:
            self.context['most_read_interviews'] = Interview.objects.most_read()
            self.context['most_read_suggestions'] = Suggestion.objects.most_read()

        return super().get(request, *args, **kwargs)


class TagView(ContextMixin, SearchMixin, TemplateView):
    template_name = 'search.html'
    paginate_by = 10
    page_request_var = 'page'
    today = timezone.now().date()
    context = {
        'today': today,
        'page_request_var': page_request_var
    }

    def get(self, request, *args, **kwargs):
        tag_slug = self.kwargs['tag'] if 'tag' in self.kwargs else ''

        self.context['interviews'] = Interview.objects.active().filter(tags__slug=tag_slug)
        self.context['suggestions'] = Suggestion.objects.active().filter(tags__slug=tag_slug)

        return super().get(request, *args, **kwargs)


class ContactFormView(SearchMixin, FormView):
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
