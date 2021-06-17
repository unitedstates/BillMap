from django.conf import settings
from django.core.mail import EmailMessage, send_mail as email_send


def send_mail(subject, to_email_list, body):
    """
        Sending email with the given data
    """

    from_email = settings.EMAIL_HOST_USER
    message = EmailMessage(subject, body, from_email, to_email_list)
    message.content_subtype = 'html'
    message.send()