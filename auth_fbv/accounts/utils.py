import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class SendEmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        super().__init__()

    def run(self):
        self.email.send()


def send_activation_email(subject, template, recipient_email, activation_url):
    from_email = 'no_reply@demomailtrap.co'
    to_email = [recipient_email]

    html_content = render_to_string(
        f'accounts/{template}.html', {'activation_url': activation_url})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    SendEmailThread(email=email).start()
