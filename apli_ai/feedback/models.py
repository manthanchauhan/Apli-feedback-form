from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.html import mark_safe
from .validators import ImageSizeValidator
from markdown import markdown


class Feedback(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True,
                             related_name='feedback_list', )
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


class FeedbackAttachedImage(models.Model):
    feedback = models.ForeignKey(to=Feedback, on_delete=models.CASCADE,
                                 related_name='images', )
    image = models.ImageField(upload_to='feedback/%y/%m/%d', validators=[
        FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'bmp']),
        ImageSizeValidator,
    ], )
