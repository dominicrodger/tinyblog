Settings
========

tinyblog has 7 relevant settings, 5 of which are required in normal
use, and 2 of which may be required.

``TINYBLOG_FROM_EMAIL``
-----------------------

Used to set the "From:" field when sending emails.

``TINYBLOG_TITLE``
------------------

Used in the RSS feed to provide the feed title.

``TINYBLOG_AUTHORNAME``
-----------------------

Used in the RSS feed for the author name and the copyright notice.

``TINYBLOG_DESCRIPTION``
------------------------

Used in the RSS feed to provide the feed description.

``TINYBLOG_AUTHORLINK``
-----------------------

Used in the RSS feed to provide a link to the post author's website
(not widely used by RSS readers).

``TINYBLOG_SITE_NAME``
----------------------

If ``django.contrib.sites`` is not in ``INSTALLED_APPS``, this setting
is required, and is used in emails sent by tinyblog.

``TINYBLOG_SITE_DOMAIN``
------------------------

.. index::
   single: TINYBLOG_SITE_DOMAIN

If ``django.contrib.sites`` is not in ``INSTALLED_APPS``, this setting
is required, and is used in emails sent by tinyblog as a link prefix.
