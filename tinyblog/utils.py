from django.conf import settings


def get_from_email():
    return settings.TINYBLOG_FROM_EMAIL
