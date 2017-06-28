from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Ονοματεπώνυμο')
    email = forms.EmailField(label='Email')
    subject = forms.CharField(label='Θέμα')
    message = forms.CharField(widget=forms.Textarea, label='Μήνυμα')
