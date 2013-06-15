from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from .utils import PostFactory


class TestPosts(TestCase):
    def test_unicode(self):
        post = PostFactory.build(title='Sample Post')
        self.assertEqual(unicode(post),
                         'Sample Post')

    def test_published(self):
        published_post = PostFactory.build(
            created=datetime(2010, 1, 1, 7, 0, 0)
        )

        self.assertTrue(published_post.published())

        unpublished_post = PostFactory.build(
            created=datetime.now() + timedelta(days=1)
        )

        self.assertFalse(unpublished_post.published())

    def test_only_valid_slugs(self):
        post = PostFactory.create(
            slug='Foobar 3'
        )

        with self.assertRaises(ValidationError):
            post.clean()

    def test_full_text(self):
        post = PostFactory.build(
            teaser_html='Hello!',
            text_html='World.'
        )

        self.assertEqual(post.full_text(),
                         'Hello!\nWorld.')

    def test_bleached_full_text(self):
        post = PostFactory.build(
            teaser_html='<a class="foo">Hello</a>!',
            text_html='<span class="western">World</span>.'
        )

        self.assertEqual(post.bleached_full_text(),
                         '<a>Hello</a>!\nWorld.')

    def test_get_teaser(self):
        post = PostFactory.build(
            text_html='Something something.'
        )

        self.assertEqual(post.get_teaser(), post.text_html)
        post.teaser_html = 'Teaser'
        self.assertEqual(post.get_teaser(), 'Teaser')
