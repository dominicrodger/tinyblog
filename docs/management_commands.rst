Management Commands
===================

``mail_subscribers``
--------------------

``mail_subscribers`` sends the oldest unsent, published blog entry to
all current e-mail subscribers (subscribers will need to have
confirmed their subscription using the link in the email they received
when they signed up, and must not have unsubscribed).

``mail_subscribers`` will only send one email to each subscriber when
it is called - if multiple entries are due to be emailed, you'll need
to run it once per entry.

You probably want to set up a cron job to run this management command
regularly - set your frequency depending on how close to the
publication time you set when creating the blog entry you wish to send
the emails.

``import_tinyblog``
-------------------

One of the URLs exposed by tinyblog is at ``json/``, which gives a
JSON dump of all published entries. You can import entries from
another blog (provided the other blog is built with tinyblog) by
running::

    django-admin.py import_tinyblog http://www.example.com/blog/json/

Duplicate entries won't be created (an entry is deemed a duplicate if
it has the same slug as an entry in the blog being imported to), so
it's safe to run this command repeatedly on the same target URL (for
example, using a cron job).
