from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^', include('tinyblog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'tests.views.test_404'
