from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

def send_email(recipients, subject, text_content, html_content):
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, recipients)
    if html_content:
        msg.attach_alternative(html_content, "text/html")
    msg.send()

def notify(booking, user, template_name):
    email_context = Context({'from': user.get_full_name(), 'booking': booking})
    text_content = get_template('notification/%s.txt'%template_name).render(email_context)
    html_content = get_template('notification/%s.html'%template_name).render(email_context)
    send_email([user.email], 'hello', text_content, html_content)