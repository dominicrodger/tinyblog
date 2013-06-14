Release Notes
*************

0.1.9 (in progress)
===================

* Re-add South migrations (removed before first publicly released
  version).
* Remove support for django-tinymce? Or add support for bleach?
* Improve pagination.
* Add support for images.

Done
----

* Add initial documentation.
* Use Travis CI for continuous integration testing.
* Removed dependence on sites framework by introducing two settings
  ``TINYBLOG_SITE_NAME`` and ``TINYBLOG_SITE_DOMAIN``. These settings
  are only required if you do not have ``django.contrib.sites`` in
  your ``INSTALLED_APPS``.

0.1.8
=====

* First version with fairly comprehensive tests.
