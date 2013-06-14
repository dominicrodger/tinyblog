from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.utils import override_settings
from tinyblog.utils import get_site_name, get_site_domain


class TestWithSitesFramework(TestCase):
    def setUp(self):
        site = Site.objects.get(pk=1)
        site.name = 'Example.com'
        site.domain = 'www.example.com'
        site.save()

    def test_get_site_name(self):
        self.assertEqual(get_site_name(),
                         'Example.com')

    def test_get_site_domain(self):
        self.assertEqual(get_site_domain(),
                         'www.example.com')


@override_settings(INSTALLED_APPS=['tinyblog', ])
class TestWithoutSitesFramework(TestCase):
    def test_get_site_domain_unconfigured(self):
        with self.assertRaises(ImproperlyConfigured):
            get_site_domain()

    @override_settings(TINYBLOG_SITE_DOMAIN='foobar.com')
    def test_get_site_domain_configured(self):
        self.assertEqual(get_site_domain(), 'foobar.com')

    def test_get_site_name_unconfigured(self):
        with self.assertRaises(ImproperlyConfigured):
            get_site_name()

    @override_settings(TINYBLOG_SITE_NAME='foobar.com')
    def test_get_site_name_configured(self):
        self.assertEqual(get_site_name(), 'foobar.com')
