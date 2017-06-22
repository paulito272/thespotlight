from django import forms
from django.contrib.auth.models import User
from django.utils.encoding import smart_text

from blog.interviews.models import Interview


class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        label = obj.username
        if obj.get_full_name():
            label = obj.get_full_name()
        return smart_text(label)


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
