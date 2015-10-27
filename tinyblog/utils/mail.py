from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from tinyblog.utils.site import (
    get_site_description,
    get_site_name
)


def get_from_email():
    return settings.TINYBLOG_FROM_EMAIL


def send_subscription_confirmation_impl(user, template_prefix):
    site = get_site_name()

    ctx = {
        'user': user,
        'site': site,
        'description': get_site_description()
    }

    subject_template = 'tinyblog/emails/%s.subj' % template_prefix
    subject = render_to_string(subject_template, ctx).strip()

    text_template = 'tinyblog/emails/%s.txt' % template_prefix
    text_content = render_to_string(text_template, ctx)

    html_template = 'tinyblog/emails/%s.html' % template_prefix
    html_content = render_to_string(html_template, ctx)

    to = user.email
    msg = EmailMultiAlternatives(subject, text_content,
                                 get_from_email(), [to, ])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_subscription_confirmation(user):
    send_subscription_confirmation_impl(user, 'confirm_subscription')
