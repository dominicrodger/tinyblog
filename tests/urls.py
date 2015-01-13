from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^', include('tinyblog.urls')),
)

handler404 = 'tests.views.test_404'
