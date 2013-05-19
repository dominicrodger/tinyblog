from django.contrib.sites.models import Site
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from tinyblog.models import Post, EmailSubscriber
from tinyblog.utils import get_from_email


class Command(BaseCommand):
    args = 'url'
    help = u'Sends the oldest unsent, published blog entry to all e-mail subscribers.'

    def generate_mail(self, post, subscriber):
        site = Site.objects.get_current()

        subject = post.title
        text_content = render_to_string('tinyblog/emails/blog_post.txt',
                                        {'user': subscriber, 'site': site, 'post': post})
        html_content = render_to_string('tinyblog/emails/blog_post.html',
                                        {'user': subscriber, 'site': site, 'post': post})
        to = subscriber.email
        msg = EmailMultiAlternatives(subject, text_content,
                                     get_from_email(), [to, ])
        msg.attach_alternative(html_content, "text/html")

        return msg

    def handle(self, *args, **options):
        posts = Post.published_objects.order_by('created').filter(emailed=False).all()

        if not posts:
            print "There are no posts to publish."
            return

        earliest_post = posts[0]

        print earliest_post.title
        mail_queue = []

        subscribers = EmailSubscriber.current_objects.all()

        for subscriber in subscribers:
            mail_queue.append(self.generate_mail(earliest_post, subscriber))

        connection = mail.get_connection()
        connection.open()

        connection.send_messages(mail_queue)
        connection.close()

        earliest_post.emailed = True
        earliest_post.save()
        print "'{0}' e-mailed to {1} subscriber(s).".format(earliest_post.title, len(subscribers))
