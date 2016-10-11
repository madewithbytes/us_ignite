from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.conf.urls import *
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

from django.contrib import admin
from us_ignite.sections import views as sections
from us_ignite.people import views as people
from us_ignite.common import views as common
# from us_ignite.blog import views as blog
from django.views.static import serve
admin.autodiscover()


# custom 404 and 500 handlers
handler404 = 'us_ignite.common.views.custom_404'
handler500 = 'us_ignite.common.views.custom_500'


urlpatterns = [
    url(r'^$', sections.home, name='home'),
    url(r'^dashboard/$', people.dashboard, name='dashboard'),
    # url('^i18n/$', set_language, name='set_language'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('us_ignite.profiles.urls')),
    url(r'^people/', include('us_ignite.people.urls')),
    url(r'^apps/', include('us_ignite.apps.urls')),
    url(r'^hub/', include('us_ignite.hubs.urls')),
    url(r'^testbed/', include('us_ignite.testbeds.urls')),
    url(r'^event/', include('us_ignite.events.urls')),
    url(r'^org/', include('us_ignite.organizations.urls')),
    url(r'^challenges/', include('us_ignite.challenges.urls')),
    url(r'^contact/', include('us_ignite.relay.urls')),
    url(r'^resources/', include('us_ignite.resources.urls')),
    # url(r'^blog/', include('us_ignite.blog.urls')),
    url(r'^search/', include('us_ignite.search.urls')),
    url(r'^map/', include('us_ignite.maps.urls')),
    url(r'^news/', include('us_ignite.news.urls')),
    url(r'^subscribe/', include('us_ignite.mailinglist.urls')),
    url(r'^overview/', include('us_ignite.visualize.urls')),
]

# Global city teams:
urlpatterns += [
    url(r'^globalcityteams/actioncluster/',
        include('us_ignite.actionclusters.urls')),
    url(r'^globalcityteams/',
        include('us_ignite.globalcityteams.urls', namespace='globalcityteams')),
    url(r'^globalcityteams/participation-guide', TemplateView.as_view(template_name='globalcityteams/participation-guide.html'))
]


urlpatterns += [
    url(r'^about/', include('us_ignite.sections.urls')),
    url(r'^get-involved/', include('us_ignite.sections.urls_get_involved')),
    url(r'^(?P<section>(about|get-involved))/(?P<slug>[-\w]+)/$',
        sections.section_page_detail,
        name='section_page_detail'),
]

urlpatterns += [
    url(r'^404/$', common.custom_404, name='http404'),
    url(r'^500/$', common.custom_500, name='http500'),
]

# Static templates:
urlpatterns += [
    url(r'^robots.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    url(r'^kit/$', TemplateView.as_view(template_name='kit.html')),
    url(r'^march2015/$', RedirectView.as_view(url='/smartfuture2015')),
    url(r'^smartfuture2015/$', TemplateView.as_view(template_name='march2015_2.html')),
    url(r'^(?i)gctcexpo/$', TemplateView.as_view(template_name='gctc-expo2016.html')),
    url(r'^(?i)gctcexpowebcast/$', TemplateView.as_view(template_name='gctc-expo_webcast.html')),
    url(r'^(?i)globalcityteamsfestival?/$', RedirectView.as_view(url='http://us-ignite.org/globalcityteamsexpo'), name='global-city-teams-expo'),
    url(r'^(?i)GCTCstrategyworkshop/$', TemplateView.as_view(template_name='gctc-strategy-workshop.html')),
    url(r'^(?i)GCTC2016Kickoff/$', TemplateView.as_view(template_name='gctc-2016-kickoff.html')),
    url(r'^(?i)smartcommunityweek/$', TemplateView.as_view(template_name='smartcommunityweek2016.html')),
    url(r'^(?i)smartcommunityweekstudent/$', TemplateView.as_view(template_name='smartcommunityweekstudent.html')),
    url(r'^(?i)smartcityworks/$', TemplateView.as_view(template_name='smartcityworks.html')),
    url(r'^awt/', include('us_ignite.advanced_wireless_testbed.urls')),

]


# US Ignite legacy redirects:
# urlpatterns += [
#     url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/$',
#         blog.legacy_redirect, name='legacy_post'),
# ]

urlpatterns += [
    url(r'^tiny_mce/(?P<path>.*)$', serve, {'document_root': 'us_ignite/assets/js/tiny_mce/'})
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^screens/$', TemplateView.as_view(template_name='screens.html')),
    ]

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]

    # Used by the debug toolbar when DEBUG is on:
    # import debug_toolbar
    # urlpatterns += [
    #     url(r'^__debug__/', include(debug_toolbar.urls)),
    # ]
