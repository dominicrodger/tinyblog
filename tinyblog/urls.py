from django.conf.urls import patterns
from tinyblog.feeds import LatestEntriesFeed
from tinyblog.views import (
    TinyBlogIndexView,
    TinyBlogYearView,
    TinyBlogMonthView,
)
from tinyblog.views.subscription import (
    TinyBlogAcknowledgeSubscriptionView
)


urlpatterns = patterns(
    '',
    (r'^$', TinyBlogIndexView.as_view(),
     {}, 'tinyblog_index'),
    (r'^(?P<year>\d{4})/$', TinyBlogYearView.as_view(),
     {}, 'tinyblog_year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', TinyBlogMonthView.as_view(),
     {}, 'tinyblog_month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>([a-z0-9-]+))/$',
     'tinyblog.views.post',
     {}, 'tinyblog_post'),
    (r'^rss/$', LatestEntriesFeed(),
     {}, 'tinyblog_rss'),
    (r'^json/$', 'tinyblog.views.jsonify',
     {}, 'tinyblog_json'),
    (r'^subscribe/$', 'tinyblog.views.subscription.subscribe',
     {}, 'tinyblog_subscribe'),
    (r'^subscribe/thanks/$', TinyBlogAcknowledgeSubscriptionView.as_view(),
     {}, 'tinyblog_subscribe_thanks'),
    (r'^subscribe/confirm/(?P<uuid>([a-z0-9]+))/$',
     'tinyblog.views.subscription.subscribe_confirm',
     {}, 'tinyblog_subscribe_confirm'),
    (r'^unsubscribe/(?P<uuid>([a-z0-9]+))/$',
     'tinyblog.views.subscription.unsubscribe',
     {}, 'tinyblog_unsubscribe'),
)
