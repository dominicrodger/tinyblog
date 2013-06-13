Installing tinyblog
===================

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
