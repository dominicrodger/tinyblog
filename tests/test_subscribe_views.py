from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from tinyblog.models import EmailSubscriber

from .utils import EmailSubscriberFactory, is_before_django_1_5


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
        self.assertContains(response, "An email is on its way")
        self.assertContains(response, subscriber.email)

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
        self.assertFalse(subscriber.unsubscribed)
        self.assertEqual(unicode(subscriber), 'to@example.com')

        self.assertEqual(response.context['subscriber'], subscriber)

    def test_unsubscribe_get_form(self):
        subscriber = EmailSubscriberFactory.create(confirmed=True)
        self.assertFalse(subscriber.unsubscribed)

        self.assertEqual(EmailSubscriber.current_objects.count(),
                         1)

        response = self.client.get(subscriber.unsubscribe_url())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context_data)
        subscriber = EmailSubscriber.objects.get(pk=subscriber.pk)
        self.assertFalse(subscriber.unsubscribed)

        self.assertEqual(EmailSubscriber.current_objects.count(),
                         1)

    def test_unsubscribe_submit_form(self):
        subscriber = EmailSubscriberFactory.create(confirmed=True)
        EmailSubscriberFactory.create(confirmed=True)
        self.assertFalse(subscriber.unsubscribed)

        self.assertEqual(EmailSubscriber.current_objects.count(),
                         2)

        response = self.client.post(
            subscriber.unsubscribe_url(),
            {'email': subscriber.email}
        )
        self.assertEqual(response.status_code, 302)
        subscriber = EmailSubscriber.objects.get(pk=subscriber.pk)
        self.assertTrue(subscriber.unsubscribed)

        self.assertEqual(EmailSubscriber.current_objects.count(),
                         0)

    def test_unsubscribe_submit_form_non_existent_email(self):
        subscriber = EmailSubscriberFactory.create(confirmed=True)
        self.assertFalse(subscriber.unsubscribed)

        self.assertEqual(EmailSubscriber.current_objects.count(),
                         1)

        response = self.client.post(
            subscriber.unsubscribe_url(),
            {'email': 'notthere@example.com'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['form'].errors['email'],
            [u'notthere@example.com is not currently subscribed.']
        )
        subscriber = EmailSubscriber.objects.get(pk=subscriber.pk)

        self.assertFalse(subscriber.unsubscribed)
        self.assertEqual(EmailSubscriber.current_objects.count(),
                         1)

    def test_unsubscribe_submit_form_bad_email_address(self):
        subscriber = EmailSubscriberFactory.create(confirmed=True)
        self.assertFalse(subscriber.unsubscribed)

        self.assertEqual(EmailSubscriber.current_objects.count(),
                         1)

        response = self.client.post(
            subscriber.unsubscribe_url(),
            {'email': 'notanemail'}
        )
        self.assertEqual(response.status_code, 200)

        if is_before_django_1_5():
            email_string = 'e-mail'
        else:
            email_string = 'email'

        self.assertEqual(
            response.context_data['form'].errors['email'],
            [u'Enter a valid %s address.' % email_string,
             u'notanemail is not currently subscribed.']
        )

        subscriber = EmailSubscriber.objects.get(pk=subscriber.pk)

        self.assertFalse(subscriber.unsubscribed)
        self.assertEqual(EmailSubscriber.current_objects.count(),
                         1)
