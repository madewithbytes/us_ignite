from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from django.contrib import admin

admin.autodiscover()


# custom 404 and 500 handlers
handler404 = 'us_ignite.common.views.custom_404'
handler500 = 'us_ignite.common.views.custom_500'

urlpatterns = patterns(
    '',
    url(r'^$', 'us_ignite.sections.views.home', name='home'),
    url(r'^dashboard/$', 'us_ignite.people.views.dashboard', name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('us_ignite.profiles.urls')),
    url(r'^people/', include('us_ignite.people.urls')),
    url(r'^apps/', include('us_ignite.apps.urls')),
    url(r'^hub/', include('us_ignite.hubs.urls')),
    url(r'^actioncluster/', include('us_ignite.actionclusters.urls')),
    url(r'^testbed/', include('us_ignite.testbeds.urls')),
    url(r'^event/', include('us_ignite.events.urls')),
    url(r'^org/', include('us_ignite.organizations.urls')),
    url(r'^challenges/', include('us_ignite.challenges.urls')),
    url(r'^contact/', include('us_ignite.relay.urls')),
    url(r'^resources/', include('us_ignite.resources.urls')),
    url(r'^blog/', include('us_ignite.blog.urls')),
    url(r'^search/', include('us_ignite.search.urls')),
    url(r'^map/', include('us_ignite.maps.urls')),
    url(r'^news/', include('us_ignite.news.urls')),
    url(r'^subscribe/', include('us_ignite.mailinglist.urls')),
    url(r'^overview/', include('us_ignite.visualize.urls')),
    url(r'^browserid/', include('django_browserid.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^about/', include('us_ignite.sections.urls')),
    url(r'^get-involved/', include('us_ignite.sections.urls_get_involved')),
    url(r'^(?P<section>(about|get-involved))/(?P<slug>[-\w]+)/$',
        'us_ignite.sections.views.section_page_detail',
        name='section_page_detail'),
)

urlpatterns += patterns(
    'us_ignite.common.views',
    url(r'^404/$', 'custom_404', name='http404'),
    url(r'^500/$', 'custom_500', name='http500'),
)

# Static templates:
urlpatterns += patterns(
    '',
    url(r'^robots.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    url(r'^kit/$', TemplateView.as_view(template_name='kit.html')),
    #url(r'^about', 'django.views.generic.simple.direct_to_template', {'template': 'path/to/about_us.html'}),)
    url(r'^globalcityteams/$', TemplateView.as_view(template_name='globalcityteams/index.html')),
    url(r'^globalcityteams/faq$', TemplateView.as_view(template_name='globalcityteams/faqs.html')),
    url(r'^globalcityteams/upload$', TemplateView.as_view(template_name='globalcityteams/document-upload.html'))
)

# US Ignite legacy redirects:
urlpatterns += patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/$',
        'us_ignite.blog.views.legacy_redirect', name='legacy_post'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^screens/$', TemplateView.as_view(template_name='screens.html')),
    )

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
