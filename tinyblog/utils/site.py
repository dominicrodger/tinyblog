from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured


def _get_site():
    return Site.objects.get_current()


def get_site_name():
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        return _get_site().name

    if not hasattr(settings, 'TINYBLOG_SITE_NAME'):
        raise ImproperlyConfigured('Please set TINYBLOG_SITE_NAME.')

    return settings.TINYBLOG_SITE_NAME


def get_site_domain():
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        return _get_site().domain

    if not hasattr(settings, 'TINYBLOG_SITE_DOMAIN'):
        raise ImproperlyConfigured('Please set TINYBLOG_SITE_DOMAIN.')

    return settings.TINYBLOG_SITE_DOMAIN
