from datetime import date
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from tinyblog.models import Post


class LatestEntriesFeed(Feed):
    def title(self):
        return settings.TINYBLOG_TITLE

    def description(self):
        return settings.TINYBLOG_DESCRIPTION

    def author_name(self):
        return settings.TINYBLOG_AUTHORNAME

    def author_link(self):
        return settings.TINYBLOG_AUTHORLINK

    def copyright(self):
        return (u'Copyright (c) %d %s.'
                % (date.now().year, settings.TINYBLOG_AUTHORNAME))

    def link(self, obj):
        return reverse('tinyblog_index')

    def items(self):
        return Post.published_objects.order_by('-created')[:15]

    def item_description(self, item):
        return item.teaser_html + item.text_html

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created
