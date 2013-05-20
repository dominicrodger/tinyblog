from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from tinyblog.models import Post, EmailSubscriber


class Command(BaseCommand):
    args = 'url'
    help = ('Sends the oldest unsent, published blog entry to '
            'all e-mail subscribers.')

    def handle(self, *args, **options):
        posts = Post.published_objects.order_by('created')
        posts = posts.filter(emailed=False).all()

        if not posts:
            print "There are no posts to publish."
            return

        earliest_post = posts[0]

        site = Site.objects.get_current()
        num_subscribers = earliest_post.mail_subscribers(site)
        print earliest_post.title

        earliest_post.emailed = True
        earliest_post.save()
        print ("'{0}' e-mailed to {1} "
               "subscriber(s).".format(earliest_post.title,
                                       num_subscribers))
