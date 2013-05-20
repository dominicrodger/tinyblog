from datetime import datetime
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.defaultfilters import truncatewords, slugify
from django.template.loader import render_to_string
from django.db import models
from uuidfield import UUIDField

from tinyblog.utils import get_from_email


class CurrentSubscribersManager(models.Manager):
    def get_query_set(self):
        return super(CurrentSubscribersManager,
                     self).get_query_set().filter(confirmed=True,
                                                  unsubscribed=False)


class EmailSubscriber(models.Model):
    email = models.EmailField()
    subscribed = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)
    unsubscribed = models.BooleanField(default=False)

    # Used for showing the e-mail address after initially signing up
    uuid_first = UUIDField(auto=True, verbose_name=u'Sign-up Key')
    # Used for confirming that this e-mail address is genuine
    uuid_second = UUIDField(auto=True, verbose_name=u'Confirmation Key')

    objects = models.Manager()
    current_objects = CurrentSubscribersManager()

    def __unicode__(self):
        return self.email

    def confirm_url(self):
        current_site = Site.objects.get_current()
        relative_url = reverse('tinyblog_subscribe_confirm',
                               args=[self.uuid_second, ])
        return u'http://{0}{1}'.format(current_site, relative_url)

    def unsubscribe_url(self):
        current_site = Site.objects.get_current()
        relative_url = reverse('tinyblog_unsubscribe',
                               args=[self.uuid_second, ])
        return u'http://{0}{1}'.format(current_site, relative_url)


class PublishedPostManager(models.Manager):
    def get_query_set(self):
        return super(PublishedPostManager,
                     self).get_query_set().filter(created__lte=datetime.now())


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_month='created')
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    teaser_html = models.TextField(verbose_name=u'Teaser')
    text_html = models.TextField(verbose_name=u'Main text')
    emailed = models.BooleanField(default=False)

    objects = models.Manager()
    published_objects = PublishedPostManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tinyblog_post',
                       args=[self.created.year,
                             '%02d' % self.created.month,
                             self.slug])

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if slugify(self.slug) != self.slug:
            raise ValidationError('Slugs must only contain lowercase '
                                  'characters, numbers and hyphens.')

    def get_teaser(self):
        if self.teaser_html:
            return self.teaser_html

        return truncatewords(self.text_html, 100)

    def full_text(self):
        return self.teaser_html + u'\n' + self.text_html

    def published(self):
        return self.created <= datetime.now()

    def generate_mail(self, subscriber, site):
        text_content = render_to_string('tinyblog/emails/blog_post.txt',
                                        {'user': subscriber,
                                         'site': site,
                                         'post': self})
        html_content = render_to_string('tinyblog/emails/blog_post.html',
                                        {'user': subscriber,
                                         'site': site,
                                         'post': self})

        msg = EmailMultiAlternatives(self.title, text_content,
                                     get_from_email(),
                                     [subscriber.email, ])
        msg.attach_alternative(html_content, "text/html")

        return msg

    def mail_subscribers(self, site):
        mail_queue = []

        subscribers = EmailSubscriber.current_objects.all()

        for subscriber in subscribers:
            mail_queue.append(self.generate_mail(subscriber, site))

        connection = mail.get_connection()
        connection.open()

        connection.send_messages(mail_queue)
        connection.close()

        return len(subscribers)

    class Meta:
        ordering = ['-created']
