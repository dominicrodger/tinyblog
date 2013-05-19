from datetime import datetime, timedelta
from django.test import TestCase
from django.core.urlresolvers import reverse
from .utils import PostFactory


class TestFeeds(TestCase):
    def test_feeds_with_entries(self):
        post1 = PostFactory.create(
            title='Published',
        )
        post2 = PostFactory.create(
            created=datetime.now() + timedelta(days=1),
            title='Unpublished',
        )
        url = reverse('tinyblog_rss')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published')
        self.assertNotContains(response, 'Unpublished')
