from django import forms

from us_ignite.apps.models import Feature
from us_ignite.hubs.models import Hub, HubRequest


class HubRequestForm(forms.ModelForm):

    class Meta:
        model = HubRequest
        fields = ('name', 'website', 'summary', 'description')


class HubForm(forms.ModelForm):
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Hub
        fields = ('name', 'website', 'summary', 'description', 'image',
                  'features', 'tags')
