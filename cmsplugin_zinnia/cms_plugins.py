"""Plugins for CMS"""
import itertools

from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.storage import staticfiles_storage

from tagging.models import TaggedItem

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from zinnia.models.entry import Entry
from zinnia.models.author import Author
from zinnia.managers import tags_published

from cmsplugin_zinnia.models import RandomEntriesPlugin
from cmsplugin_zinnia.models import LatestEntriesPlugin
from cmsplugin_zinnia.models import SelectedEntriesPlugin
from cmsplugin_zinnia.models import QueryEntriesPlugin
from cmsplugin_zinnia.models import CalendarEntriesPlugin
from cmsplugin_zinnia.forms import CalendarEntriesAdminForm


class ZinniaCMSPluginBase(CMSPluginBase):
    """
    Base plugin for cmsplugin_zinnia
    """
    module = 'Zinnia'
    text_enabled = True

    def icon_src(self, instance):
        """
        Base icon for Zinnia's plugins
        """
        return staticfiles_storage.url('cmsplugin_zinnia/img/plugin.png')


class CMSLatestEntriesPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including the latest entries filtered
    """
    model = LatestEntriesPlugin
    name = _('Latest entries')
    render_template = 'cmsplugin_zinnia/entry_list.html'
    filter_horizontal = ['categories', 'authors', 'tags']
    fieldsets = (
        (None, {'fields': (
            ('number_of_entries', 'offset'),
            'template_to_render')}),
        (_('Filters'), {'fields': (
            'featured',
            ('categories', 'subcategories'),
            'authors', 'tags'),
         'classes': ('collapse',)}),)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Filtering manytomany field
        """
        if db_field.name == 'authors':
            kwargs['queryset'] = Author.published.all()
        if db_field.name == 'tags':
            kwargs['queryset'] = tags_published()
        return super(CMSLatestEntriesPlugin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def render(self, context, instance, placeholder):
        """
        Update the context with plugin's data
        """
        entries = Entry.published.all()

        if instance.categories.count():
            cats = instance.categories.all()

            if instance.subcategories:
                cats = itertools.chain(cats, *[c.get_descendants()
                                               for c in cats])

            entries = entries.filter(categories__in=cats)
        if instance.authors.count():
            entries = entries.filter(authors__in=instance.authors.all())
        if instance.tags.count():
            entries = TaggedItem.objects.get_union_by_model(
                entries, instance.tags.all())

        if instance.featured is not None:
            entries = entries.filter(featured=instance.featured)

        entries = entries.distinct()
        if instance.offset:
            entries = entries[instance.offset:]
        if instance.number_of_entries:
            entries = entries[:instance.number_of_entries]

        context = super(CMSLatestEntriesPlugin, self).render(
            context, instance, placeholder)
        context['entries'] = entries
        return context


class CMSSelectedEntriesPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including a selection of entries
    """
    model = SelectedEntriesPlugin
    name = _('Selected entries')
    render_template = 'cmsplugin_zinnia/entry_list.html'
    fields = ('entries', 'template_to_render')
    filter_horizontal = ['entries']

    def render(self, context, instance, placeholder):
        """
        Update the context with plugin's data
        """
        context = super(CMSSelectedEntriesPlugin, self).render(
            context, instance, placeholder)
        context['entries'] = instance.entries.all()
        return context


class CMSRandomEntriesPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including random entries
    """
    model = RandomEntriesPlugin
    name = _('Random entries')
    render_template = 'cmsplugin_zinnia/entries_random.html'
    fields = ('number_of_entries', 'template_to_render')

    def render(self, context, instance, placeholder):
        """
        Update the context with plugin's data
        """
        context = super(CMSRandomEntriesPlugin, self).render(
            context, instance, placeholder)
        context['template_to_render'] = (str(instance.template_to_render) or
                                         'zinnia/tags/entries_random.html')
        return context


class CMSQueryEntriesPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including entries based on a search query
    """
    model = QueryEntriesPlugin
    name = _('Query entries')
    render_template = 'cmsplugin_zinnia/entry_list.html'
    fields = ('query', 'number_of_entries', 'template_to_render')

    def render(self, context, instance, placeholder):
        """
        Update the context with plugin's data
        """
        entries = Entry.published.search(instance.query)
        if instance.number_of_entries:
            entries = entries[:instance.number_of_entries]

        context = super(CMSQueryEntriesPlugin, self).render(
            context, instance, placeholder)
        context['entries'] = entries
        return context


class CMSCalendarEntriesPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including calendar of published entries
    """
    model = CalendarEntriesPlugin
    name = _('Calendar entries')
    render_template = 'cmsplugin_zinnia/entries_calendar.html'
    fieldsets = ((None, {
        'fields': (('year', 'month'),),
        'description': _("If you don't set year and month, "
                         "the current month will be used.")}),)
    form = CalendarEntriesAdminForm


class CMSSearchPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including a Zinnia's search form
    """
    name = _('Entries search form')
    render_template = 'cmsplugin_zinnia/search_form.html'

    def icon_alt(self, instance):
        """
        Alternative text of the plugin
        """
        return self.name


class CMSToolsPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including tool links for Zinnia
    """
    name = _('Administration tools')
    render_template = 'cmsplugin_zinnia/tools.html'

    def icon_alt(self, instance):
        """
        Alternative text of the plugin
        """
        return self.name


class CMSPublishedCategoriesPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including Zinnia's published categories
    """
    name = _('Published categories')
    render_template = 'cmsplugin_zinnia/categories_published.html'


class CMSTreeCategoriesPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including Zinnia's categories as a tree
    """
    name = _('Categories tree')
    render_template = 'cmsplugin_zinnia/categories_tree.html'


class CMSPublishedAuthorsPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including Zinnia's published authors
    """
    name = _('Published authors')
    render_template = 'cmsplugin_zinnia/authors_published.html'


class CMSTagCloudPlugin(ZinniaCMSPluginBase):
    """
    Plugin for including Zinnia's tag cloud
    """
    name = _('Tag cloud')
    render_template = 'cmsplugin_zinnia/tag_cloud.html'


class CMSArchivesTreePlugin(ZinniaCMSPluginBase):
    """
    Plugin for including an archive tree
    """
    name = _('Archives tree')
    render_template = 'cmsplugin_zinnia/entries_archives_tree.html'


plugin_pool.register_plugin(CMSLatestEntriesPlugin)
plugin_pool.register_plugin(CMSSelectedEntriesPlugin)
plugin_pool.register_plugin(CMSRandomEntriesPlugin)
plugin_pool.register_plugin(CMSQueryEntriesPlugin)
plugin_pool.register_plugin(CMSCalendarEntriesPlugin)
plugin_pool.register_plugin(CMSSearchPlugin)
plugin_pool.register_plugin(CMSToolsPlugin)
plugin_pool.register_plugin(CMSTreeCategoriesPlugin)
plugin_pool.register_plugin(CMSPublishedCategoriesPlugin)
plugin_pool.register_plugin(CMSPublishedAuthorsPlugin)
plugin_pool.register_plugin(CMSTagCloudPlugin)
plugin_pool.register_plugin(CMSArchivesTreePlugin)
