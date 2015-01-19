from django.conf.urls import patterns
from tinyblog.feeds import LatestEntriesFeed


urlpatterns = patterns(
    '',
    (r'^$', 'tinyblog.views.index_view',
     {}, 'tinyblog_index'),
    (r'^(?P<year>\d{4})/$', 'tinyblog.views.year_view',
     {}, 'tinyblog_year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'tinyblog.views.month_view',
     {}, 'tinyblog_month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>([a-z0-9-]+))/$',
     'tinyblog.views.post',
     {}, 'tinyblog_post'),
    (r'^rss/$', LatestEntriesFeed(),
     {}, 'tinyblog_rss'),
    (r'^json/$', 'tinyblog.views.json.serialized_posts',
     {}, 'tinyblog_json'),
    (r'^subscribe/$', 'tinyblog.views.subscription.subscribe',
     {}, 'tinyblog_subscribe'),
    (r'^subscribe/thanks/$',
     'tinyblog.views.subscription.acknowledge_subscription',
     {}, 'tinyblog_subscribe_thanks'),
    (r'^subscribe/confirm/(?P<uuid>([a-z0-9]+))/$',
     'tinyblog.views.subscription.subscribe_confirm',
     {}, 'tinyblog_subscribe_confirm'),
    (r'^unsubscribe/thanks/$',
     'tinyblog.views.subscription.unsubscribe_thanks',
     {}, 'tinyblog_unsubscribe_thanks'),
    (r'^unsubscribe/$',
     'tinyblog.views.subscription.unsubscribe',
     {}, 'tinyblog_unsubscribe'),
)
