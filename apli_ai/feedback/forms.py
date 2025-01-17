from django import forms
from django_summernote.widgets import SummernoteWidget


class FeedbackForm(forms.Form):
    username = forms.CharField(label='Username', required=True,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Your username'}
                               ))

    email = forms.EmailField(label='Email id', required=True,
                             widget=forms.EmailInput(
                                 attrs={'placeholder': 'Your registered e-mail id'}
                             ))

    subject = forms.CharField(label='Subject', max_length=100, required=True,
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Describe your issue in short'}
                              ))

    message = forms.CharField(label='Message', required=True,
                              widget=SummernoteWidget)

    image = forms.ImageField(required=False, label='Upload an image',
                             help_text='Provide an optional image (less than 8 MB)')
