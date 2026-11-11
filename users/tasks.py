from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def deactivate_inactive_users():
    """Блокирует пользователей, не заходивших более месяца."""
    threshold = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=threshold,
        is_active=True,
    )
    count = inactive_users.update(is_active=False)
    return f'Заблокировано: {count}'