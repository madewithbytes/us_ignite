from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.event_list, name='event_list'),
    url(r'^past/$', views.event_list, {'timeframe': 'past'},
        name='event_list_past'),
    url(r'^add/$', views.event_add, name='event_add'),
    url(r'^(?P<slug>[-\w]+)/$', views.event_detail, name='event_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.event_edit, name='event_edit'),
    url(r'^(?P<slug>[-\w]+)/ics/$', views.event_detail_ics,
        name='event_detail_ics'),
]
