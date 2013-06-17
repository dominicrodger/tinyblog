from datetime import datetime, timedelta
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy
import feedparser
from .utils import PostFactory


class TestFeeds(TestCase):
    url = reverse_lazy('tinyblog_rss')

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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published')
        self.assertNotContains(response, 'Unpublished')
        self.assertContains(response, "href")
        self.assertNotContains(response, "class")
        self.assertNotContains(response, "span")

    def test_simple_entry_gives_valid_rss(self):
        PostFactory.create(
            title='Simple Entry',
            teaser_html='foobar',
            text_html='baz'
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        parsed = feedparser.parse(response.content)
        self.assertNotEqual(parsed.bozo, 1)
        self.assertEqual(len(parsed['entries']), 1)
        self.assertEqual(parsed['entries'][0]['title'], 'Simple Entry')

    def test_entry_with_html_gives_valid_rss(self):
        PostFactory.create(
            title='Entry with HTML',
            teaser_html='<a href="#">foobar</a>',
            text_html='<strong>baz</strong>'
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check validity
        parsed = feedparser.parse(response.content)
        self.assertNotEqual(parsed.bozo, 1)
        self.assertEqual(len(parsed['entries']), 1)
        self.assertEqual(parsed['entries'][0]['title'], 'Entry with HTML')
        self.assertEqual(parsed['entries'][0]['summary'],
                         '<a href="#">foobar</a>\n<strong>baz</strong>')

    def test_entry_with_invalid_html_gives_valid_rss(self):
        PostFactory.create(
            title='Entry with Invalid HTML',
            teaser_html='<a href="#">foobar',
            text_html='baz</strong>'
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check validity
        parsed = feedparser.parse(response.content)
        self.assertNotEqual(parsed.bozo, 1)
        self.assertEqual(len(parsed['entries']), 1)
        self.assertEqual(parsed['entries'][0]['title'],
                         'Entry with Invalid HTML')
        self.assertEqual(parsed['entries'][0]['summary'],
                         '<a href="#">foobar\nbaz</a>')
