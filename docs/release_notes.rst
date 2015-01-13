Release Notes
*************

0.3.1 (planned)
===============

* Figure out how to include all the Disqus JavaScript if
  ``TINYBLOG_DISQUS_SHORTNAME`` is set.
* Improve pagination.
* Add support for images.

0.3.0
=====

* Drop Python 2.6 support (it may still work, but is no longer
  supported).
* Switch test format to py.test.
* Add support for Django 1.6.
* RSS feeds now contain bleached post content (with this release, all
  places where HTML is output are now passed through bleach).
* Add tests to ensure generated RSS is valid with bad HTML, using
  feedparser.

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
