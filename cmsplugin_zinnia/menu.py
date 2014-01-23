"""Menus for cmsplugin_zinnia"""
from django.utils.dateformat import format
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.utils.translation import ugettext_lazy as _

from menus.base import Modifier
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

from zinnia.models.entry import Entry
from zinnia.models.author import Author
from zinnia.models.category import Category
from zinnia.managers import tags_published
from cmsplugin_zinnia.settings import HIDE_ENTRY_MENU


class EntryMenu(CMSAttachMenu):
    """
    Menu for the entries organized by archives dates
    """
    name = _('Zinnia Entry Menu')

    def get_nodes(self, request):
        """
        Return menu's node for entries
        """
        nodes = []
        archives = []
        attributes = {'hidden': HIDE_ENTRY_MENU}
        for entry in Entry.published.all():
            year = entry.creation_date.strftime('%Y')
            month = entry.creation_date.strftime('%m')
            month_text = format(entry.creation_date, 'b').capitalize()
            day = entry.creation_date.strftime('%d')

            key_archive_year = 'year-%s' % year
            key_archive_month = 'month-%s-%s' % (year, month)
            key_archive_day = 'day-%s-%s-%s' % (year, month, day)

            if not key_archive_year in archives:
                nodes.append(NavigationNode(
                    year, reverse('zinnia_entry_archive_year', args=[year]),
                    key_archive_year, attr=attributes))
                archives.append(key_archive_year)

            if not key_archive_month in archives:
                nodes.append(NavigationNode(
                    month_text,
                    reverse('zinnia_entry_archive_month', args=[year, month]),
                    key_archive_month, key_archive_year,
                    attr=attributes))
                archives.append(key_archive_month)

            if not key_archive_day in archives:
                nodes.append(NavigationNode(
                    day, reverse('zinnia_entry_archive_day',
                                 args=[year, month, day]),
                    key_archive_day, key_archive_month,
                    attr=attributes))
                archives.append(key_archive_day)

            nodes.append(NavigationNode(entry.title, entry.get_absolute_url(),
                                        entry.pk, key_archive_day))
        return nodes


class CategoryMenu(CMSAttachMenu):
    """
    Menu for the categories
    """
    name = _('Zinnia Category Menu')

    def get_nodes(self, request):
        """
        Return menu's node for categories
        """
        nodes = []
        nodes.append(NavigationNode(_('Categories'),
                                    reverse('zinnia_category_list'),
                                    'categories'))
        for category in Category.objects.all():
            nodes.append(NavigationNode(category.title,
                                        category.get_absolute_url(),
                                        category.pk, 'categories'))
        return nodes


class AuthorMenu(CMSAttachMenu):
    """
    Menu for the authors
    """
    name = _('Zinnia Author Menu')

    def get_nodes(self, request):
        """
        Return menu's node for authors
        """
        nodes = []
        nodes.append(NavigationNode(_('Authors'),
                                    reverse('zinnia_author_list'),
                                    'authors'))
        for author in Author.published.all():
            nodes.append(NavigationNode(author.__unicode__(),
                                        author.get_absolute_url(),
                                        author.pk, 'authors'))
        return nodes


class TagMenu(CMSAttachMenu):
    """
    Menu for the tags
    """
    name = _('Zinnia Tag Menu')

    def get_nodes(self, request):
        """
        Return menu's node for tags
        """
        nodes = []
        nodes.append(NavigationNode(_('Tags'), reverse('zinnia_tag_list'),
                                    'tags'))
        for tag in tags_published():
            nodes.append(NavigationNode(tag.name,
                                        reverse('zinnia_tag_detail',
                                                args=[tag.name]),
                                        tag.pk, 'tags'))
        return nodes


class EntryModifier(Modifier):
    """
    Menu Modifier for entries,
    hide the MenuEntry in navigation,
    not in breadcrumbs
    """

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        """
        Modify nodes of a menu
        """
        if breadcrumb:
            return nodes
        for node in nodes:
            if node.attr.get('hidden'):
                node.visible = False
        return nodes


menu_pool.register_menu(EntryMenu)
menu_pool.register_menu(CategoryMenu)
menu_pool.register_menu(AuthorMenu)
menu_pool.register_menu(TagMenu)
menu_pool.register_modifier(EntryModifier)


def invalidate_menu_cache(sender, **kwargs):
    """
    Signal receiver to invalidate the menu_pool
    cache when an entry is posted
    """
    menu_pool.clear()

post_save.connect(
    invalidate_menu_cache, sender=Entry,
    dispatch_uid='zinnia.entry.postsave.invalidate_menu_cache')
post_delete.connect(
    invalidate_menu_cache, sender=Entry,
    dispatch_uid='zinnia.entry.postdelete.invalidate_menu_cache')
