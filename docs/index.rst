Welcome to tinyblog's documentation!
====================================

tinyblog is a Django app for single-author blogging. It has three key
features:

1. **Delayed publication:** Set a date and time when you want your
   blog entry to be published.
2. **Email lists:** Allow users to subscribe to email updates,
   tinyblog will handle confirmation of email addresses, and will
   always include unsubscribe links in any emails it sends.
3. **Syndication:** tinyblog allows you to have the same content on
   multiple sites, by exposing a JSON feed of posts, and allowing you
   to import from that JSON feed from other sites.

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   management_commands
   settings
   release_notes
