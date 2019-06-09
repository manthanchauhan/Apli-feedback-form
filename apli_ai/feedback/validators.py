from django.core.exceptions import ValidationError
from django.conf import settings


def ImageSizeValidator(image_field):
    max_size = settings.MAX_IMAGE_SIZE

    if image_field.size > max_size:
        raise ValidationError('Image size should be less than 8MB')
