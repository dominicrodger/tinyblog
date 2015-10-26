from django.core.management.base import NoArgsCommand
from tinyblog.models import Post


class Command(NoArgsCommand):
    help = ('Sends the oldest unsent, published blog entry to '
            'all e-mail subscribers.')

    def handle_noargs(self, *args, **options):
        try:
            post = Post.get_next_post_to_email()
        except Post.DoesNotExist:
            print "There are no posts to publish."
            return

        seen_subscribers = post.mail_subscribers()

        post.emailed = True
        post.save()

        if not seen_subscribers:
            print ("'{0}' e-mailed to 0 subscriber(s).".format(
                post.title
            ))
        else:
            print ("'{0}' e-mailed to {1} "
                   "subscriber(s):".format(post.title,
                                           len(seen_subscribers)))
            print ('\n'.join(seen_subscribers))
