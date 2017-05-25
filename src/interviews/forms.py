from django import forms
from django.contrib.auth.models import User
from django.utils.encoding import smart_text

from .models import Interview


class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name())


class InterviewModelForm(forms.ModelForm):
    author = UserFullnameChoiceField(queryset=User.objects.all())

    class Meta:
        model = Interview
        fields = [
            'author',
            'interviewee',
            'category',
            'title',
            'content',
            'draft',
            'publish',
            'slug'
        ]
