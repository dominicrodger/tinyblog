from datetime import datetime, timedelta
from django.test import TestCase
from django.core.urlresolvers import reverse
from .utils import PostFactory


class TestFeeds(TestCase):
    def test_feeds_with_entries(self):
        PostFactory.create(
            title='Published',
            teaser_html='<a href="foo">Hello</a>!',
            text_html='<span class="western">World</span>.'
        )
        PostFactory.create(
            created=datetime.now() + timedelta(days=1),
            title='Unpublished',
        )
        url = reverse('tinyblog_rss')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published')
        self.assertNotContains(response, 'Unpublished')
        self.assertContains(response, "href")
        self.assertNotContains(response, "class")
        self.assertNotContains(response, "span")
