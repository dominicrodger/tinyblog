from datetime import datetime, timedelta
from django.test import TestCase
from django.core import serializers
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from .utils import PostFactory


class TestBasicViews(TestCase):
    def test_index_with_no_entries(self):
        url = reverse('tinyblog_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_index_with_entries(self):
        PostFactory.create(
            teaser_html='<a class="foo">Hello</a>!',
            text_html='<span class="western">World</span>.'
        )
        url = reverse('tinyblog_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'western')
        self.assertNotContains(response, 'foo')
        self.assertContains(response, 'Hello')
        self.assertNotContains(response, 'World')
        self.assertNotContains(response, 'disqus')

    @override_settings(TINYBLOG_DISQUS_SHORTNAME='foobar')
    def test_index_with_entries_and_disqus(self):
        PostFactory.create(
            teaser_html='<a class="foo">Hello</a>!',
            text_html='<span class="western">World</span>.'
        )
        url = reverse('tinyblog_index')
        response = self.client.get(url)
        self.assertContains(response, 'disqus')

    def test_post_detail(self):
        post = PostFactory.create(
            teaser_html='<a class="foo">Hello</a>!',
            text_html='<span class="western">World</span>.'
        )
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'western')
        self.assertNotContains(response, 'foo')
        self.assertContains(response, 'Hello')
        self.assertContains(response, 'World')
        self.assertNotContains(response, 'disqus')

    @override_settings(TINYBLOG_DISQUS_SHORTNAME='foobar')
    def test_post_detail_with_disqus(self):
        post = PostFactory.create(
            teaser_html='<a class="foo">Hello</a>!',
            text_html='<span class="western">World</span>.'
        )
        response = self.client.get(post.get_absolute_url())
        self.assertContains(response, 'disqus')

    def test_uncreated_post_detail(self):
        post = PostFactory.create(created=datetime.now() + timedelta(days=1))
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_year_index_with_no_entries(self):
        url = reverse('tinyblog_year', args=['2012', ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_year_index_with_entries(self):
        PostFactory.create()
        url = reverse('tinyblog_year', args=['2013', ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_month_index_with_no_entries(self):
        url = reverse('tinyblog_month', args=['2012', '01'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_month_index_with_entries(self):
        PostFactory.create()
        url = reverse('tinyblog_month', args=['2013', '01'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_post_json(self):
        post1 = PostFactory.create()
        post2 = PostFactory.create()
        post3 = PostFactory.create()
        later = datetime.now() + timedelta(days=1)
        post4 = PostFactory.create(created=later)

        url = reverse('tinyblog_json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        posts = [p.object.title
                 for p in serializers.deserialize("json", response.content)]

        self.assertEqual(len(posts), 3)

        self.assertTrue(post1.title in posts)
        self.assertTrue(post2.title in posts)
        self.assertTrue(post3.title in posts)
        self.assertFalse(post4.title in posts)
