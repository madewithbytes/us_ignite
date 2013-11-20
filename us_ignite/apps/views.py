from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods


from us_ignite.apps.forms import (ApplicationForm, ApplicationLinkFormSet,
                                  MembershipForm, ApplicationImageFormSet)
from us_ignite.apps.models import (Application, ApplicationMembership,
                                   ApplicationVersion)
from us_ignite.common import pagination, forms


APPS_SORTING_CHOICES = (
    ('', 'Select ordering'),
    ('name', 'Name a-z'),
    ('-name', 'Name z-a'),
)


def app_list(request):
    """Lists the published ``Applications``"""
    page_no = pagination.get_page_no(request.GET)
    order_form = forms.OrderForm(
        request.GET, order_choices=APPS_SORTING_CHOICES)
    order_value = order_form.cleaned_data['order'] if order_form.is_valid() else ''
    object_list = Application.objects.filter(status=Application.PUBLISHED)
    if order_value:
        # TODO consider using non case-sensitive ordering:
        object_list = object_list.order_by(order_value)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'order': order_value,
        'order_form': order_form,
    }
    return TemplateResponse(request, 'apps/object_list.html', context)


def get_app_for_user(slug, user):
    """Validates the user can access the given app."""
    app = get_object_or_404(Application.active, slug__exact=slug)
    # Application is published, no need for validation:
    if app.is_visible_by(user):
        return app
    raise Http404


def app_detail(request, slug):
    app = get_app_for_user(slug, request.user)
    context = {
        'object': app,
        'url_list': app.applicationurl_set.all(),
        'image_list': app.applicationimage_set.all(),
        'member_list': app.members.select_related('profile').all(),
        'version_list': app.applicationversion_set.all(),
        'can_edit': app.is_editable_by(request.user),
        'is_owner': app.is_owned_by(request.user),
    }
    return TemplateResponse(request, 'apps/object_detail.html', context)


@login_required
def app_add(request):
    """View for adding an ``Application``."""
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(
                request, 'The application "%s" has been added.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = ApplicationForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'apps/object_add.html', context)


@login_required
def app_edit(request, slug):
    app = get_object_or_404(Application.active, slug__exact=slug)
    if not app.is_editable_by(request.user):
        raise Http404
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=app)
        link_formset = ApplicationLinkFormSet(request.POST, instance=app)
        image_formset = ApplicationImageFormSet(
            request.POST, request.FILES, instance=app)
        if (form.is_valid() and link_formset.is_valid()
            and image_formset.is_valid()):
            instance = form.save()
            link_formset.save()
            image_formset.save()
            messages.success(
                request, 'The application "%s" has been updated.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = ApplicationForm(instance=app)
        link_formset = ApplicationLinkFormSet(instance=app)
        image_formset = ApplicationImageFormSet(instance=app)
    context = {
        'object': app,
        'form': form,
        'link_formset': link_formset,
        'image_formset': image_formset,
    }
    return TemplateResponse(request, 'apps/object_edit.html', context)


@require_http_methods(["POST"])
@login_required
def app_version_add(request, slug):
    app = get_object_or_404(Application.active, slug__exact=slug)
    if not app.is_editable_by(request.user):
        raise Http404
    ApplicationVersion.objects.create_version(app)
    messages.success(request, 'Application has been versioned.')
    return redirect(app.get_absolute_url())


def app_version_detail(request, slug, version_slug):
    app = get_app_for_user(slug, request.user)
    # Determine if the slug provided is a valid version:
    version = None
    version_list = []
    for version_obj in app.applicationversion_set.all():
        if version_obj.slug == version_slug:
            version = version_obj
        else:
            version_list.append(version_obj)
    if not version:
        raise Http404
    context = {
        'object': version,
        'version_list': version_list,
        'app': app,
    }
    return TemplateResponse(request, 'apps/object_version_detail.html', context)


def create_member(app, user):
    """Create a new member when it is unexistent and return it."""
    membership, is_new = (ApplicationMembership.objects
                          .get_or_create(application=app, user=user))
    return membership if is_new else None


@login_required
def app_membership(request, slug):
    """Adds collaborators to an application."""
    app = get_object_or_404(
        Application.active, slug__exact=slug, owner=request.user)
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            membership = []
            for member in form.cleaned_data['collaborators']:
                membership.append(create_member(app, member))
            total_members = len(filter(None, membership))
            messages.success(
                request, 'Added %s new collaborators.' % total_members)
            return redirect(app.get_membership_url())
    else:
        form = MembershipForm()
    membership_list = (app.applicationmembership_set
                       .select_related('user', 'application', 'user__profile')
                       .all())
    context = {
        'object': app,
        'membership_list': membership_list,
        'form': form,
    }
    return TemplateResponse(request, 'apps/object_membership.html', context)


@require_http_methods(["POST"])
@login_required
def app_membership_remove(request, slug, membership_id):
    """Removes the given user from the given app."""
    membership = get_object_or_404(
        ApplicationMembership.objects.select_related('application'),
        application__slug__exact=slug, application__owner=request.user,
        pk=membership_id)
    redirect_url = membership.application.get_membership_url()
    membership.delete()
    messages.success(request, 'Removed collaborator.')
    return redirect(redirect_url)
