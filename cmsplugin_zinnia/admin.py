"""Admin of Zinnia CMS Plugins"""
from django.contrib import admin
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from cms.plugin_rendering import render_placeholder
from cms.admin.placeholderadmin import PlaceholderAdminMixin

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin
from zinnia.settings import ENTRY_BASE_MODEL


class EntryPlaceholderAdmin(PlaceholderAdminMixin, EntryAdmin):
    """
    EntryPlaceholder Admin
    """
    fieldsets = (
        (_('Content'), {'fields': (('title', 'status'), 'image')}),) + \
        EntryAdmin.fieldsets[1:]

    def save_model(self, request, entry, form, change):
        """
        Fill the content field with the interpretation
        of the placeholder
        """
        context = RequestContext(request)
        try:
            content = render_placeholder(entry.content_placeholder, context)
            entry.content = content or ''
        except KeyError:
            # https://github.com/django-blog-zinnia/cmsplugin-zinnia/pull/61
            entry.content = ''
        super(EntryPlaceholderAdmin, self).save_model(
            request, entry, form, change)


if ENTRY_BASE_MODEL == 'cmsplugin_zinnia.placeholder.EntryPlaceholder':
    admin.site.register(Entry, EntryPlaceholderAdmin)
