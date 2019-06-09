from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.contrib import messages

from . import views
from . import settings
from . import models


class FeedBackTest(TestCase):
    def setUp(self):
        self.url = reverse('feedback:feedback_form')
        self.test_user = User.objects.create_user(username='somemoreuser', email='someemail@django.com',
                                                  password='somerandompassword', )

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, f'feedback form status code is '
                                                    f'{response.status_code}'
                         )

    def test_view_func(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, views.FeedbackView)

    def test_csrf(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_no_render(self):
        response = self.client.post(self.url, {'username': self.test_user.username,
                                               'email': self.test_user.email,
                                               'subject': 'test',
                                               'message': 'test-message'
                                               })
        self.assertEqual(response.status_code, 200, f'response status code is '
                                                    f'{response.status_code}')
        self.assertTemplateUsed(response, 'feedback/form.html')

        all_messages = [m.message for m in messages.get_messages(response.wsgi_request)]
        self.assertIn(settings.NO_CAPTCHA_ERROR, all_messages)

    def test_invalid_user_render(self):
        response = self.client.post(self.url, {'username': 'wrongusername',
                                               'email': self.test_user.email,
                                               'subject': 'subject',
                                               'message': 'test-message',
                                               'reCAPTCHA': True
                                               })
        self.assertEqual(response.status_code, 200, f'response status code is '
                                                    f'{response.status_code}')
        self.assertTemplateUsed(response, 'feedback/form.html')
        all_messages = [m.message for m in messages.get_messages(response.wsgi_request)]
        self.assertIn(settings.INVALID_USERNAME_ERROR, all_messages)

    def test_successful_feedback(self):
        response = self.client.post(self.url, {'username': self.test_user.username,
                                               'email': self.test_user.email,
                                               'subject': 'subject',
                                               'message': 'test-message',
                                               'reCAPTCHA': True
                                               })
        self.assertEqual(len(models.Feedback.objects.filter(subject='subject')), 1,
                         f'feedback is not created in database')
        url = reverse('home')
        self.assertRedirects(response, url)




