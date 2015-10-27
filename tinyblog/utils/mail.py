from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from tinyblog.utils.site import get_site_name


def get_from_email():
    return settings.TINYBLOG_FROM_EMAIL


def send_subscription_confirmation(user):
    site = get_site_name()

    subject = 'Thanks for subscribing to {0}'.format(site)

    ctx = {
        'user': user,
        'site': site
    }

    text_template = 'tinyblog/emails/confirm_subscription.txt'
    text_content = render_to_string(text_template, ctx)

    html_template = 'tinyblog/emails/confirm_subscription.html'
    html_content = render_to_string(html_template, ctx)

    to = user.email
    msg = EmailMultiAlternatives(subject, text_content,
                                 get_from_email(), [to, ])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
