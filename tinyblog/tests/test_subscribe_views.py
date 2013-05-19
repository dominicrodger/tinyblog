from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from tinyblog.models import EmailSubscriber

from .utils import EmailSubscriberFactory


class TestSubscribeViews(TestCase):
    def test_subscribe_get(self):
        url = reverse('tinyblog_subscribe')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_subscribe_bad_post(self):
        self.assertEqual(EmailSubscriber.objects.all().count(),
                         0)
        url = reverse('tinyblog_subscribe')
        response = self.client.post(url,
                                    {'email': 'toexample.com'})
        self.assertEqual(response.status_code, 200)

    def test_subscribe_post(self):
        self.assertEqual(EmailSubscriber.objects.all().count(),
                         0)
        url = reverse('tinyblog_subscribe')
        response = self.client.post(url,
                                    {'email': 'to@example.com'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(EmailSubscriber.objects.all().count(),
                         1)

        subscriber = EmailSubscriber.objects.get(pk=1)
        self.assertFalse(subscriber.confirmed)
        self.assertFalse(subscriber.unsubscribed)
        self.assertEqual(unicode(subscriber), 'to@example.com')

        self.assertEqual(response.context['subscriber'], subscriber)

        self.assertEqual(response.request['PATH_INFO'],
                         reverse('tinyblog_subscribe_thanks'))

        self.assertEqual(len(mail.outbox), 1)

        themail = mail.outbox[0]
        self.assertEqual(themail.subject,
                         'Thanks for subscribing to example.com')
        self.assertEqual(themail.to,
                         ['to@example.com', ])
        self.assertEqual(themail.from_email,
                         'from@example.com')
        self.assertTrue(themail.body.index(str(subscriber.uuid_second)) > 0)
        self.assertTrue(themail.body.index(subscriber.confirm_url()) > 0)
        self.assertTrue(themail.body.index(subscriber.unsubscribe_url()) > 0)

    def test_subscribe_confirm(self):
        subscriber = EmailSubscriberFactory.create()
        self.assertFalse(subscriber.confirmed)
        response = self.client.get(subscriber.confirm_url())
        self.assertEqual(response.status_code, 200)
        subscriber = EmailSubscriber.objects.get(pk=subscriber.pk)
        self.assertTrue(subscriber.confirmed)

    def test_unsubscribe(self):
        subscriber = EmailSubscriberFactory.create(confirmed=True)
        self.assertFalse(subscriber.unsubscribed)
        response = self.client.get(subscriber.unsubscribe_url())
        self.assertEqual(response.status_code, 200)
        subscriber = EmailSubscriber.objects.get(pk=subscriber.pk)
        self.assertTrue(subscriber.unsubscribed)