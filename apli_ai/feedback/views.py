from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from . import forms
from . import models
from . import settings as feedback_settings


class FeedbackView(View):
    form_class = forms.FeedbackForm
    template = 'feedback/form.html'

    def get(self, request):
        initial = {}
        if request.user.is_authenticated:
            initial['username'] = request.user.username
            initial['email'] = request.user.email

        form = self.form_class(initial=initial)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if 'reCAPTCHA' not in request.POST.keys():
            messages.error(request, feedback_settings.NO_CAPTCHA_ERROR)
            return render(request, self.template, {'form': form})

        if form.is_valid():
            form_data = form.cleaned_data

            try:
                user = User.objects.get(username=form_data['username'])
            except ObjectDoesNotExist:
                messages.error(request, feedback_settings.INVALID_USERNAME_ERROR)
                return render(request, self.template, {'form': form})

            image = request.FILES.get('image', None)
            max_size = settings.MAX_IMAGE_SIZE
            max_size_MB = max_size//(1024*1024)

            if image is not None and image.size > max_size:
                messages.error(request, 'Image is too big, please keep the size of the image'
                                        f'less that {str(max_size_MB)} MB')
                form = self.form_class()
                return render(request, self.template, {'form': form})

            feedback = models.Feedback.objects.create(user=user,
                                                      subject=form_data['subject'],
                                                      message=form_data['message'],
                                                      )
            if image is not None:
                image = models.FeedbackAttachedImage.objects.create(feedback=feedback,
                                                                    image=request.FILES['image'])

            messages.success(request, 'You feedback has been submitted successfully!')
            self.send_mail_to_operations(feedback, image, user)
            self.send_mail_to_user(user, feedback)
            return redirect('home')

        else:
            form = self.form_class(request.POST, request.FILES)
            return render(request, self.template, {'form': form})

    def send_mail_to_user(self, user, feedback):
        subject = 'Feedback submitted successfully'
        message_template = 'feedback/user_email.html'
        message = render_to_string(message_template, {'user': user,
                                                      'feedback_id': feedback.id,
                                                      'app_name': 'Apli.ai',
                                                      })
        email = EmailMessage(subject=subject, body=message,
                             from_email=settings.EMAIL_HOST_USER,
                             to=[user.email], )
        email.content_subtype = 'html'
        email.send()

    def send_mail_to_operations(self, feedback, image, user):
        subject = 'feedback submitted by ' + user.username
        message_template = 'feedback/operations_email.html'
        message = render_to_string(message_template, {'user': user,
                                                      'feedback': feedback
                                                      })
        email = EmailMessage(subject=subject, body=message,
                             from_email=settings.EMAIL_HOST_USER,
                             to=[settings.OPERATIONS_EMAIL],
                             )
        email.content_subtype = 'html'

        if image is not None:
            email.attach_file(path=image.image.url[1:])
        email.send()


class Home(View):
    def get(self, request):
        return render(request, 'index.html')