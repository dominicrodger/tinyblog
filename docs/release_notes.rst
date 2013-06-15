Release Notes
*************

0.1.9 (in progress)
===================

* Improve pagination.
* Add support for images.
* Find a way to test South migrations with tox.

Done
----

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
