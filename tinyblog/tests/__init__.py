from django.test import TestCase
from django.core.urlresolvers import reverse


class SimpleTest(TestCase):
    def test_index_with_no_entries(self):
        url = reverse('tinyblog_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
