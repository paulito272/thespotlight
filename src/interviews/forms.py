from django import forms
from django.forms import widgets

from .models import Interview


class CustomDateInput(widgets.DateInput):
    input_type = 'date'


class InterviewForm(forms.ModelForm):
    publish = forms.DateField(widget=CustomDateInput)

    class Meta:
        model = Interview
        fields = [
            'author',
            'interviewee',
            'title',
            'content',
            'draft',
            'publish',
        ]
