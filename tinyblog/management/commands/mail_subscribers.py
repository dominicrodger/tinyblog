from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from tinyblog.models import Post


class Command(BaseCommand):
    help = ('Sends the oldest unsent, published blog entry to '
            'all e-mail subscribers.')

    def handle(self, *args, **options):
        try:
            post = Post.get_next_post_to_email()
        except Post.DoesNotExist:
            print "There are no posts to publish."
            return

        site = Site.objects.get_current()
        num_subscribers = post.mail_subscribers(site)

        post.emailed = True
        post.save()

        print ("'{0}' e-mailed to {1} "
               "subscriber(s).".format(post.title,
                                       num_subscribers))
