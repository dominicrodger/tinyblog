from django.conf import settings
from django.contrib.sites.models import Site


def get_from_email():
    return settings.TINYBLOG_FROM_EMAIL


def get_site():
    return Site.objects.get_current()


def get_site_name():
    return get_site().name
