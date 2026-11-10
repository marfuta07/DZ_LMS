from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_course_update_email(course_title: str, user_emails: list):
    """Отправляет письмо подписчикам курса при обновлении."""
    subject = f'Курс "{course_title}" обновлён'
    message = f'Материалы курса "{course_title}" были обновлены. Заходите посмотреть!'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        user_emails,
        fail_silently=False,
    )