from django.test import TestCase
from tinyblog.utils import tinyblog_bleach


class TestBleach(TestCase):
    def test_notags(self):
        self.assertEqual(tinyblog_bleach('foobar'),
                         'foobar')

    def test_no_classes(self):
        self.assertEqual(tinyblog_bleach('<strong class="western">'
                                         'foo'
                                         '</strong>'),
                         '<strong>foo</strong>')

    def test_links_work(self):
        self.assertEqual(tinyblog_bleach('<a class="cat" href="bar">'
                                         'foo'
                                         '</a>'),
                         '<a href="bar">foo</a>')
