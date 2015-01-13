Installing tinyblog
===================

tinyblog supports Python 2.7, and Django 1.4, 1.5 and 1.6. Python 3
support is blocked waiting for django-uuidfield to support Python 3.

tinyblog is available on PyPI, so can be installed into a virtualenv
with pip like this::

    pip install tinyblog

Once you've installed tinyblog, just add it to your
``INSTALLED_APPS``, and set up your ``urls.py`` to reference it::

    urlpatterns = patterns(
        '',
        ...
        url(r'^blog/', include('tinyblog.urls')),
    )

To integrate tinyblog with your site's templates, override
``tinyblog/base.html``. tinyblog expects the main content block to be
called ``contents``.
