"""Toolbar extensions for CMS"""
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


class ZinniaToolbar(CMSToolbar):

    def populate(self):
        zinnia_menu = self.toolbar.get_or_create_menu(
            'zinnia-menu', _('Zinnia'))

        url = reverse('admin:zinnia_entry_add')
        zinnia_menu.add_sideframe_item(_('New entry'), url=url)

        url = reverse('admin:zinnia_category_add')
        zinnia_menu.add_sideframe_item(_('New category'), url=url)

        zinnia_menu.add_break()

        url = reverse('admin:zinnia_entry_changelist')
        zinnia_menu.add_sideframe_item(_('Entries list'), url=url)

        url = reverse('admin:zinnia_category_changelist')
        zinnia_menu.add_sideframe_item(_('Categories list'), url=url)

        url = reverse('admin:tagging_tag_changelist')
        zinnia_menu.add_sideframe_item(_('Tags list'), url=url)


toolbar_pool.register(ZinniaToolbar)
