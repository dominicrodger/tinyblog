from django.conf import settings
from django.contrib.sites.models import Site


def get_from_email():
    return settings.TINYBLOG_FROM_EMAIL


def _get_site():
    site = Site.objects.get_current()
    return {
        'domain': site.domain,
        'name': site.name
    }


def get_site_name():
    return _get_site()['name']


def get_site_domain():
    return _get_site()['domain']
