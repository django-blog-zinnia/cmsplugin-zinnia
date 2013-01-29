"""Plugins for CMS"""
import itertools

from django.conf import settings
from django.utils.translation import ugettext as _

from tagging.models import TaggedItem

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from cms.models.pluginmodel import CMSPlugin

from zinnia.models import Entry
from zinnia.models import Author
from zinnia.managers import tags_published

from cmsplugin_zinnia.models import RandomEntriesPlugin
from cmsplugin_zinnia.models import LatestEntriesPlugin
from cmsplugin_zinnia.models import SelectedEntriesPlugin
from cmsplugin_zinnia.models import QueryEntriesPlugin
from cmsplugin_zinnia.models import CalendarEntriesPlugin
from cmsplugin_zinnia.forms import CalendarEntriesAdminForm


class CMSLatestEntriesPlugin(CMSPluginBase):
    """Plugin for including the latest entries filtered"""
    module = 'Zinnia'
    model = LatestEntriesPlugin
    name = _('Latest entries')
    render_template = 'cmsplugin_zinnia/entry_list.html'
    filter_horizontal = ['categories', 'authors', 'tags']
    fieldsets = (
        (None, {'fields': ('number_of_entries',
                           'template_to_render')}),
        (_('Filters'), {'fields': (('categories', 'subcategories'),
                                   'authors', 'tags'),
                        'classes': ('collapse',)}),)
    text_enabled = True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filtering manytomany field"""
        if db_field.name == 'authors':
            kwargs['queryset'] = Author.published.all()
        if db_field.name == 'tags':
            kwargs['queryset'] = tags_published()
        return super(CMSLatestEntriesPlugin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
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

        entries = entries.distinct()
        if instance.number_of_entries:
            entries = entries[:instance.number_of_entries]
        context.update({'entries': entries,
                        'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'cmsplugin_zinnia/img/plugin.png'


class CMSSelectedEntriesPlugin(CMSPluginBase):
    """Plugin for including a selection of entries"""
    module = 'Zinnia'
    model = SelectedEntriesPlugin
    name = _('Selected entries')
    render_template = 'cmsplugin_zinnia/entry_list.html'
    fields = ('entries', 'template_to_render')
    filter_horizontal = ['entries']
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        context.update({'entries': instance.entries.all(),
                        'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'cmsplugin_zinnia/img/plugin.png'


class CMSRandomEntriesPlugin(CMSPluginBase):
    """Plugin for including random entries"""
    module = 'Zinnia'
    model = RandomEntriesPlugin
    name = _('Random entries')
    render_template = 'cmsplugin_zinnia/random_entries.html'
    fields = ('number_of_entries', 'template_to_render')
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        context.update(
            {'object': instance,
             'placeholder': placeholder,
             'template_to_render': str(instance.template_to_render) or
             'zinnia/tags/random_entries.html'})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'cmsplugin_zinnia/img/plugin.png'


class CMSQueryEntriesPlugin(CMSPluginBase):
    """Plugin for including random entries"""
    module = 'Zinnia'
    model = QueryEntriesPlugin
    name = _('Query entries')
    render_template = 'cmsplugin_zinnia/entry_list.html'
    fields = ('query', 'number_of_entries', 'template_to_render')
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        entries = Entry.published.search(instance.query)
        if instance.number_of_entries:
            entries = entries[:instance.number_of_entries]

        context.update({'entries': entries,
                        'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'cmsplugin_zinnia/img/plugin.png'


class CMSCalendarEntriesPlugin(CMSPluginBase):
    """Plugin for including calendar of published entries"""
    module = 'Zinnia'
    model = CalendarEntriesPlugin
    name = _('Calendar entries')
    render_template = 'cmsplugin_zinnia/calendar.html'
    fieldsets = ((None, {
        'fields': (('year', 'month'),),
        'description': _("If you don't set year and month, "
                         "the current month will be used.")}),)
    form = CalendarEntriesAdminForm
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        context.update({'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'cmsplugin_zinnia/img/plugin.png'


class CMSSearchPlugin(CMSPluginBase):
    """Plugins for including a Zinnia's search form"""
    module = 'Zinnia'
    model = CMSPlugin
    name = _('Entries search form')
    render_template = 'cmsplugin_zinnia/search_form.html'
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        context.update({'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_alt(self, instance):
        """Alternative text of the plugin"""
        return unicode(self.name)

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'cmsplugin_zinnia/img/plugin.png'


class CMSToolsPlugin(CMSPluginBase):
    """Plugins for including tool links for Zinnia"""
    module = 'Zinnia'
    model = CMSPlugin
    name = _('Administration tools')
    render_template = 'cmsplugin_zinnia/tools.html'
    text_enabled = True

    def render(self, context, instance, placeholder):
        """Update the context with plugin's data"""
        context.update({'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_alt(self, instance):
        """Alternative text of the plugin"""
        return unicode(self.name)

    def icon_src(self, instance):
        """Icon source of the plugin"""
        return settings.STATIC_URL + u'cmsplugin_zinnia/img/plugin.png'


plugin_pool.register_plugin(CMSLatestEntriesPlugin)
plugin_pool.register_plugin(CMSSelectedEntriesPlugin)
plugin_pool.register_plugin(CMSRandomEntriesPlugin)
plugin_pool.register_plugin(CMSQueryEntriesPlugin)
plugin_pool.register_plugin(CMSCalendarEntriesPlugin)
plugin_pool.register_plugin(CMSSearchPlugin)
plugin_pool.register_plugin(CMSToolsPlugin)
