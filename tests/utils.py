from datetime import datetime
import django
from django.core.management import call_command
import factory
from StringIO import StringIO
import sys
from tinyblog.models import Post, EmailSubscriber


class PostFactory(factory.Factory):
    FACTORY_FOR = Post

    title = factory.Sequence(lambda n: 'Post %s' % n)
    slug = factory.Sequence(lambda n: 'post-%s' % n)
    created = datetime(2013, 1, 1, 7, 0, 0)


class EmailSubscriberFactory(factory.Factory):
    FACTORY_FOR = EmailSubscriber

    email = 'to@example.com'


class OutputRedirector(object):
    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self.obj
        sys.stderr = self.obj

    def __exit__(self, type, value, traceback):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr


def run_command_for_test(command, *args):
    content = StringIO()

    with OutputRedirector(content):
        call_command(command, *args, stdout=content, stderr=content)

    content.seek(0)
    return content.read().strip()


def is_before_django_1_5():
    version = django.VERSION

    if version[0] > 1:
        return False

    return version[1] < 5
