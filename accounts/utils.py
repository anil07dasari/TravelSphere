import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now
from accounts.models import CustomUser


class EmailService(object):

    def send_email(self, email, uuid):
        subject = 'Reset your password'
        user = CustomUser.objects.filter(email=email).first()
        expiration_time = now() + datetime.timedelta(hours=24)
        recipient = email
        context = {
            'firstname': user.first_name,
            'reset_link': f"{settings.RESET_PASSWORD_URL}?token={uuid}&expiry={expiration_time.timestamp()}"
        }
        html_message = render_to_string('email/reset_password.html', context)
        plain_message = strip_tags(html_message)
        try:
            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [recipient],
                      fail_silently=False, html_message=html_message)
        except Exception as e:
            print(e)

    def password_reset_confirm(self, user, subject):
        subject = subject
        recipient = user.email
        context = {
            'firstname': user.first_name,
        }
        html_message = render_to_string('email/password_reset_success_email.html', context)
        plain_message = strip_tags(html_message)
        try:
            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [recipient],
                      fail_silently=False, html_message=html_message)
        except Exception as e:
            print(e)