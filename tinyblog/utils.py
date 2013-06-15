from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
import bleach


def get_from_email():
    return settings.TINYBLOG_FROM_EMAIL


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


DEFAULT_TINYBLOG_ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'p',
    'strong',
    'ul',
]


DEFAULT_TINYBLOG_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
}


def tinyblog_bleach(content):
    if hasattr(settings, 'TINYBLOG_NO_BLEACH'):
        if settings.TINYBLOG_NO_BLEACH:
            return content

    allowed_tags = DEFAULT_TINYBLOG_ALLOWED_TAGS

    if hasattr(settings, 'TINYBLOG_ALLOWED_TAGS'):
        allowed_tags = settings.TINYBLOG_ALLOWED_TAGS

    allowed_attributes = DEFAULT_TINYBLOG_ALLOWED_ATTRIBUTES

    if hasattr(settings, 'TINYBLOG_ALLOWED_ATTRIBUTES'):
        allowed_attributes = settings.TINYBLOG_ALLOWED_ATTRIBUTES

    return bleach.clean(content,
                        tags=allowed_tags,
                        attributes=allowed_attributes,
                        strip=True)
