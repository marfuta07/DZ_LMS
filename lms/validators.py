from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    """Разрешает только ссылки на youtube.com."""
    if value and 'youtube.com' not in value:
        raise ValidationError('Ссылка должна вести на youtube.com')