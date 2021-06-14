from celery import shared_task
from common.util.mailer import send_mail

@shared_task(bind=True)
def send_email(self, subject, emails, content):
    """Sending email"""
    send_mail(subject, emails, content)

    return f"Email sent to: {emails}"