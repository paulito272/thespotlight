from django import forms
from django.forms import widgets
from pagedown.widgets import PagedownWidget

from .models import Interview


class CustomDateInput(widgets.DateInput):
    input_type = 'date'


class InterviewForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(widget=CustomDateInput)

    class Meta:
        model = Interview
        fields = [
            'title',
            'interviewee',
            'content',
            'draft',
            'publish',
        ]
