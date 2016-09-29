"""Admin of Zinnia CMS Plugins"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin

from zinnia.models import Entry
from zinnia.admin.entry import EntryAdmin
from zinnia.settings import ENTRY_BASE_MODEL


class EntryPlaceholderAdmin(PlaceholderAdminMixin, EntryAdmin):
    """
    EntryPlaceholder Admin
    """
    fieldsets = (
        (_('Content'), {'fields': (('title', 'status'), 'image')}),) + \
        EntryAdmin.fieldsets[1:]


if ENTRY_BASE_MODEL == 'cmsplugin_zinnia.placeholder.EntryPlaceholder':
    admin.site.register(Entry, EntryPlaceholderAdmin)
