"""Admin of Zinnia CMS Plugins"""
from django.contrib import admin
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from cms.plugin_rendering import render_placeholder
from cms.admin.placeholderadmin import PlaceholderAdmin

from zinnia.models import Entry
from zinnia.admin.entry import EntryAdmin
from zinnia.settings import ENTRY_BASE_MODEL


class EntryPlaceholderAdmin(PlaceholderAdmin, EntryAdmin):
    """EntryPlaceholder Admin"""
    fieldsets = ((None, {'fields': ('title', 'image', 'status')}),
                 (_('Content'), {'fields': ('content_placeholder',),
                                 'classes': ('plugin-holder',
                                             'plugin-holder-nopage')})) + \
                                             EntryAdmin.fieldsets[1:]

    def save_model(self, request, entry, form, change):
        """Fill the content field with the interpretation
        of the placeholder"""
        context = RequestContext(request)
        entry.content = render_placeholder(entry.content_placeholder, context)
        super(EntryPlaceholderAdmin, self).save_model(
            request, entry, form, change)


if ENTRY_BASE_MODEL == 'cmsplugin_zinnia.placeholder.EntryPlaceholder':
    admin.site.unregister(Entry)
    admin.site.register(Entry, EntryPlaceholderAdmin)
