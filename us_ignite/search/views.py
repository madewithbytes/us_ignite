import json
import watson

from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt

from us_ignite.apps.models import Application
from us_ignite.common import pagination
from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub
from us_ignite.actionclusters.models import ActionCluster
from us_ignite.organizations.models import Organization
from us_ignite.resources.models import Resource
from us_ignite.search.filters import tag_search
from us_ignite.search.forms import SearchForm

from taggit.models import Tag


@csrf_exempt
def search_apps(request):
    return tag_search(
        request, Application.active.filter(status=Application.PUBLISHED),
        'search/application_list.html')


@csrf_exempt
def search_events(request):
    return tag_search(request, Event.published, 'search/event_list.html')


@csrf_exempt
def search_hubs(request):
    return tag_search(request, Hub.active, 'search/hub_list.html')


@csrf_exempt
def search_actionclusters(request):
    return tag_search(
        request, ActionCluster.active, 'search/actioncluster_list.html')


@csrf_exempt
def search_organizations(request):
    return tag_search(
        request, Organization.active, 'search/organization_list.html')


@csrf_exempt
def search_resources(request):
    return tag_search(
        request, Resource.published, 'search/resource_list.html')


SEARCH_PARAMS = {
    'default': (),
    'globalcities': (
        ActionCluster,
        Event.published.filter(section=Event.GLOBALCITIES),
    ),
}


def get_search_results(query, slug):
    if slug not in SEARCH_PARAMS:
        raise Http404('Invalid search slug.')
    models = SEARCH_PARAMS[slug]
    object_list = list(watson.search(query, models=models))
    # Perform the search with the rest of the models:
    if models:
        object_list += list(watson.search(query, exclude=models))
    return object_list


@csrf_exempt
def search(request, slug='default'):
    form = SearchForm(request.GET) if 'q' in request.GET else SearchForm()
    page_no = pagination.get_page_no(request.GET)
    if form.is_valid():
        object_list = get_search_results(form.cleaned_data['q'], slug)
        pagination_qs = '&%s' % urlencode({'q': form.cleaned_data['q']})
    else:
        object_list = []
        pagination_qs = ''
    page = pagination.get_page(object_list, page_no)
    page.object_list_top = [o.object for o in page.object_list_top]
    page.object_list_bottom = [o.object for o in page.object_list_bottom]
    context = {
        'form': form,
        'page': page,
        'pagination_qs': pagination_qs,
    }
    return TemplateResponse(request, 'search/object_list.html', context)


@csrf_exempt
def tag_list(request):
    object_list = Tag.objects.filter(is_featured=True).order_by('name')
    object_list = [t.name for t in object_list]
    return HttpResponse(
        json.dumps(object_list), content_type='application/javascript')
