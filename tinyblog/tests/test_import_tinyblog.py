import django
from datetime import datetime
from django.core import mail
from django.core import serializers
from django.core.management.base import CommandError
from django.test import TestCase
from mock import Mock, patch
from requests.exceptions import ConnectionError
from django.utils.unittest import skipIf
from tinyblog.models import Post
from .utils import test_command, PostFactory


def is_before_django_1_5():
    version = django.VERSION

    if version[0] > 1:
        return False

    return version[1] < 5


class FakeResponse(object):
    def __init__(self, status, resp):
        self.status_code = status
        self.content = resp


@skipIf(is_before_django_1_5(),
        "Failed management commands call sys.exit(1) in Django 1.4")
class TestImportTinyblog(TestCase):
    def test_without_args(self):
        with self.assertRaises(CommandError):
            test_command("import_tinyblog")

    def test_with_invalid_url(self):
        with self.assertRaises(CommandError):
            test_command("import_tinyblog", "foobar")

    def test_with_url_that_returns_failure(self):
        def get_fake_response(k):
            return FakeResponse(400, 'Something went wrong')

        with patch('requests.get', Mock(side_effect=get_fake_response)):
            with self.assertRaises(CommandError):
                test_command("import_tinyblog", "http://test/")

    def test_with_object_that_does_exist(self):
        PostFactory.create(title='Sample Post', slug='foobar')

        def get_fake_response(k):
            data = serializers.serialize("json", Post.published_objects.all())
            return FakeResponse(200, data)

        with patch('requests.get', Mock(side_effect=get_fake_response)):
            result = test_command("import_tinyblog", "http://test/")
            self.assertEqual(result, ("Processing \"Sample Post\"...\n"
                                      "Already had existing object with "
                                      "the slug \"foobar\"."))

    def test_with_object_that_does_not_exist(self):
        PostFactory.create(title='Sample Post')
        data = serializers.serialize("json", Post.published_objects.all())

        def get_fake_response(k):
            return FakeResponse(200, data)

        Post.objects.all().delete()

        with patch('requests.get', Mock(side_effect=get_fake_response)):
            result = test_command("import_tinyblog", "http://test/")
            self.assertEqual(result, ("Processing \"Sample Post\"...\n"
                                      "Saved new object."))
