"""Forms for cmsplugin-zinnia"""
from django import forms
from django.utils.translation import ugettext as _

from cmsplugin_zinnia.models import CalendarEntriesPlugin


class CalendarEntriesAdminForm(forms.ModelForm):
    """
    Admin Form for CalendarEntriesPlugin
    """

    def clean(self):
        data = self.cleaned_data
        if int(bool(data.get('year'))) + int(bool(data.get('month'))) == 1:
            raise forms.ValidationError(
                _('Year and month must defined together.'))
        return data

    class Meta:
        model = CalendarEntriesPlugin
        fields = forms.ALL_FIELDS
