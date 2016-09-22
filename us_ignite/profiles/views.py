import uuid

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from registration import signals
from registration.backends.default import views as registration_views
from registration.models import RegistrationProfile
from registration.views import ActivationView as BaseActivationView

from us_ignite.apps.models import Application
from us_ignite.common import decorators
from us_ignite.events.models import Event
from us_ignite.profiles import forms
from us_ignite.profiles.models import Profile
from us_ignite.resources.models import Resource


def get_uuid():
    """Removing the reduced size bytes to reduce the risk of collisions.

    More: http://en.wikipedia.org/wiki/Universally_unique_identifier
    #Version_4_.28random.29"""
    stream = uuid.uuid4().hex
    return stream[:12] + stream[13:16] + stream[17:]


class EmailRegistrationView(registration_views.RegistrationView):
    form_class = forms.UserRegistrationForm

    def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        email, password = cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        # Generate a random username, email is used for login:
        username = get_uuid()
        new_user = (RegistrationProfile.objects
                    .create_inactive_user(username, email, password, site))
        new_user.first_name = cleaned_data['first_name']
        new_user.last_name = cleaned_data['last_name']
        new_user.save()
        signals.user_registered.send(
            sender=self.__class__, user=new_user, request=request)
        return new_user


class ActivationView(BaseActivationView):

    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.
        """
        activated_user = RegistrationProfile.objects.activate_user(activation_key)
        return activated_user

    def get_success_url(self, request, user):
        return ('registration_activation_complete', (), {})

# Registration views:
# Using function aliases for lazy loadind and readability in the urls file.
registration_view = decorators.not_auth_required(
    EmailRegistrationView.as_view())
registration_activation_complete = TemplateView.as_view(
    template_name='registration/activation_complete.html')
# Using local ``Activation`` view to avoid sending duplicate
# user_activated signals:
registration_activate = ActivationView.as_view()
registration_complete = TemplateView.as_view(
    template_name='registration/registration_complete.html')
registration_disallowed = TemplateView.as_view(
    template_name='registration/registration_closed.html')


@login_required
def user_profile(request):
    """Edit the ``User`` owned ``Profile``."""
    # Make sure the user has a profile:
    profile, is_new = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        formset = forms.ProfileLinkFormSet(request.POST, instance=profile)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Thank you for updating your Profile.')
            return redirect('user_profile')
    else:
        form = forms.ProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
        })
        formset = forms.ProfileLinkFormSet(instance=profile)
    context = {
        'object': profile,
        'form': form,
        'formset': formset,
    }
    return TemplateResponse(request, 'profile/user_profile.html', context)


@login_required
def user_profile_delete(request):
    """Removes the authenticated ``User`` details."""
    # List of the content to be disassociated:
    application_list = Application.objects.filter(owner=request.user)
    event_list = Event.objects.filter(user=request.user)
    resource_list = Resource.objects.filter(contact=request.user)
    if request.method == 'POST':
        request.user.delete()
        # Logut user
        logout(request)
        msg = 'Your account and all associated data has been removed.'
        messages.success(request, msg)
        return redirect('home')
    context = {
        'application_list': application_list,
        'event_list': event_list,
        'resource_list': resource_list,
    }
    return TemplateResponse(
        request, 'profile/user_profile_delete.html', context)
