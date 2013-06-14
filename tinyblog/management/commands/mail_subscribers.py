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

        num_subscribers = post.mail_subscribers()

        post.emailed = True
        post.save()

        print ("'{0}' e-mailed to {1} "
               "subscriber(s).".format(post.title,
                                       num_subscribers))
