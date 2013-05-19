from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
import requests
from tinyblog.models import Post


class Command(BaseCommand):
    args = 'url'
    help = u'Fetches blog entries from <url>, and loads them into tinyblog.'

    def handle(self, *args, **options):
        if not args:
            raise CommandError(u"You must provide a URL.")

        url = args[0]

        r = requests.get(url)

        if r.status_code != 200:
            raise CommandError(u"Received status {0} from {1}, expected 200.".format(r.status_code, url))

        for obj in serializers.deserialize("json", r.content):
            self.stdout.write(u'Processing "{0}"...\n'.format(obj.object.title))
            try:
                Post.objects.get(slug=obj.object.slug)
                self.stdout.write(u'Already had existing object with the slug "{0}".\n'.format(obj.object.slug))
            except Post.DoesNotExist:
                obj.save()
                self.stdout.write(u'Saved new object.\n')
