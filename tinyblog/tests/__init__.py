from datetime import datetime, timedelta
from django.test import TestCase
from django.core.urlresolvers import reverse
from tinyblog.models import Post
import factory


class PostFactory(factory.Factory):
    FACTORY_FOR = Post

    title = factory.Sequence(lambda n: 'Post %s' % n)
    slug = factory.Sequence(lambda n: 'post-%s' % n)
    created = datetime(2013, 1, 1, 7, 0, 0)


class SimpleTest(TestCase):
    def test_index_with_no_entries(self):
        url = reverse('tinyblog_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_index_with_entries(self):
        post = PostFactory.create()
        url = reverse('tinyblog_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        post = PostFactory.create()
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_uncreated_post_detail(self):
        post = PostFactory.create(created=datetime.now() + timedelta(days=1))
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_year_index_with_no_entries(self):
        url = reverse('tinyblog_year', args=['2012', ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_year_index_with_entries(self):
        post = PostFactory.create()
        url = reverse('tinyblog_year', args=['2013', ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_month_index_with_no_entries(self):
        url = reverse('tinyblog_month', args=['2012', '01'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_month_index_with_entries(self):
        post = PostFactory.create()
        url = reverse('tinyblog_month', args=['2013', '01'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
