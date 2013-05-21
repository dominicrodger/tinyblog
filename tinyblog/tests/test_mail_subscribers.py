from datetime import datetime
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from StringIO import StringIO
import sys

from .utils import PostFactory, EmailSubscriberFactory


def mail_subscribers():
    content = StringIO()
    original_stdout = sys.stdout
    sys.stdout = content
    call_command("mail_subscribers", stdout=content)
    content.seek(0)
    sys.stdout = original_stdout
    return content.read().strip()


class TestMailSubscribers(TestCase):
    def test_no_posts(self):
        self.assertEqual(mail_subscribers(),
                         "There are no posts to publish.")

    def test_no_subscribers(self):
        PostFactory.create(title='Sample Post')
        printed = mail_subscribers()
        self.assertEqual(printed,
                         "'Sample Post' e-mailed to 0 subscriber(s).")

    def test_with_subscribers(self):
        PostFactory.create(title='Mail Everyone (already sent)',
                           created=datetime(2011, 1, 1, 7, 0, 0),
                           emailed=True)
        PostFactory.create(title='Mail Everyone',
                           created=datetime(2012, 1, 1, 7, 0, 0))
        PostFactory.create(title='Mail Everyone (newer)',
                           created=datetime(2013, 1, 1, 7, 0, 0))

        subscriber1 = EmailSubscriberFactory.create(
            email='to1@example.com',
            confirmed=True,
        )

        subscriber2 = EmailSubscriberFactory.create(
            email='to2@example.com',
            confirmed=True,
        )

        EmailSubscriberFactory.create(
            email='not_subscribed@example.com',
            confirmed=False,
        )

        EmailSubscriberFactory.create(
            email='unsubscribed@example.com',
            confirmed=True,
            unsubscribed=True,
        )

        printed = mail_subscribers()
        self.assertEqual(printed,
                         "'Mail Everyone' e-mailed to 2 subscriber(s).")

        self.assertEqual(len(mail.outbox), 2)

        self.assertEqual(mail.outbox[0].subject,
                         'Mail Everyone')
        self.assertEqual(mail.outbox[1].subject,
                         'Mail Everyone')

        self.assertEqual(mail.outbox[0].to,
                         ['to1@example.com', ])
        self.assertEqual(mail.outbox[1].to,
                         ['to2@example.com', ])
        self.assertEqual(mail.outbox[0].from_email,
                         'from@example.com')
        self.assertEqual(mail.outbox[1].from_email,
                         'from@example.com')

        unsubscribe_url1 = subscriber1.unsubscribe_url()
        unsubscribe_url2 = subscriber2.unsubscribe_url()
        self.assertTrue(mail.outbox[0].body.index(unsubscribe_url1) > 0)
        self.assertTrue(mail.outbox[1].body.index(unsubscribe_url2) > 0)
