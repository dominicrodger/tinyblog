Release Notes
*************

0.1.9 (in progress)
===================

* Remove support for django-tinymce? Or add support for bleach?
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

0.1.8
=====

* First version with fairly comprehensive tests.
