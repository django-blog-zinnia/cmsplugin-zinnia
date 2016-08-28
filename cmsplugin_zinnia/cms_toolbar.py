"""Toolbar extensions for CMS"""
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


class ZinniaToolbar(CMSToolbar):

    def populate(self):
        user = self.request.user
        zinnia_menu = self.toolbar.get_or_create_menu(
            'zinnia-menu', _('Zinnia'))

        if user.has_perm('zinnia.add_entry'):
            url = reverse('admin:zinnia_entry_add')
            zinnia_menu.add_sideframe_item(_('New entry'), url=url)

        if user.has_perm('zinnia.add_category'):
            url = reverse('admin:zinnia_category_add')
            zinnia_menu.add_sideframe_item(_('New category'), url=url)

        if zinnia_menu.get_items():
            zinnia_menu.add_break()

        if user.has_perm('zinnia.change_entry'):
            url = reverse('admin:zinnia_entry_changelist')
            zinnia_menu.add_sideframe_item(_('Entries list'), url=url)

        if user.has_perm('zinnia.change_category'):
            url = reverse('admin:zinnia_category_changelist')
            zinnia_menu.add_sideframe_item(_('Categories list'), url=url)

        if user.has_perm('tagging.change_tag'):
            url = reverse('admin:tagging_tag_changelist')
            zinnia_menu.add_sideframe_item(_('Tags list'), url=url)

        if not zinnia_menu.get_items():
            self.toolbar.remove_item(zinnia_menu)


toolbar_pool.register(ZinniaToolbar)
