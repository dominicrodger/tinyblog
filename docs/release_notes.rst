Release Notes
*************

0.next (planned)
================

* Figure out how to include all the Disqus JavaScript if
  ``TINYBLOG_DISQUS_SHORTNAME`` is set.
* Improve pagination.
* Add support for images.

0.5.0
=====

* Drop support for Django 1.4, 1.5 and 1.6.
* Add a new view for inviting people to subscribe to the blog - this
  sends out a slightly differently worded message, to avoid
  confusion.
* Switch the last function-based view over to class-based views.

0.4.5
=====

* Fix for people subscribing multiple times - let's ensure people
  only get a single email, and that unsubscribing works.
* Print out each email address that had emails sent when running
  ``mail_subscribers``.

0.4.4
=====

* Allow searching on email address in the admin.

0.4.3
=====

* Ensure Disqus works over HTTPS, by using protocol-relative URLs.

0.4.2
=====

* Add Django 1.8 support.

0.4.1
=====

* Fix a bug in the unsubscribe page with the link for going back to
  the blog (the ``url`` tag was split over two lines, so the link
  didn't render correctly).

0.4.0
=====

* Help prevent inadvertent unsubscriptions from link
  pre-fetchers/forwarded emails by requiring an email address be
  entered to complete cancellation of a subscription.
* Remove the need for UUIDs in the unsubscription code (this will
  break old unsubscribe links).

0.3.0
=====

* Drop Python 2.6 support (it may still work, but is no longer
  supported).
* Switch test format to py.test.
* Add support for Django 1.6 and Django 1.7.
* RSS feeds now contain bleached post content (with this release, all
  places where HTML is output are now passed through bleach).
* Add tests to ensure generated RSS is valid with bad HTML, using
  feedparser.
* Removed South migrations - they aren't currently used (we only have
  an initial version), and this will smooth the way to switching to
  using Django 1.7's new migrations feature.

0.2.0
=====

* Add settings for allowed tags (``TINYBLOG_ALLOWED_TAGS``) and
  allowed attributes (``TINYBLOG_ALLOWED_ATTRIBUTES``) in bleach.
* Added a setting for not bleaching content at all
  (``TINYBLOG_NO_BLEACH``).
* Default to allowing the ``p`` tag through.

0.1.9
=====

If you're using South, and have an existing installation of 0.1.8
you'll need to run after installing, otherwise future migrations will
fail::

    python manage.py migrate tinyblog --fake

* Added initial documentation.
* Set up Travis CI integration for continuous integration testing.
* Removed dependence on sites framework by introducing two settings
  ``TINYBLOG_SITE_NAME`` and ``TINYBLOG_SITE_DOMAIN``. These settings
  are only required if you do not have ``django.contrib.sites`` in
  your ``INSTALLED_APPS``.
* Re-added South migrations (removed before first publicly released
  version).
* Added support for bleach (if you have overriden tinyblog templates,
  you may wish to access ``bleached_teaser``, ``bleached_text`` and
  ``bleached_full_text``, rather than ``teaser_html``, ``text_html``
  and ``full_text`` respectively). Text is stored as input (i.e. with
  any bad tags or attributes), and cleaned on output.

0.1.8
=====

* First version with fairly comprehensive tests.
