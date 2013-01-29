"""Models of Zinnia CMS Plugins"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.utils.translation import ugettext_lazy as _

from tagging.models import Tag
from cms.models import CMSPlugin
from menus.menu_pool import menu_pool

from zinnia.models import Entry
from zinnia.models import Category

from cmsplugin_zinnia.settings import PLUGINS_TEMPLATES

TEMPLATES = [
    ('cmsplugin_zinnia/entry_list.html', _('Entry list (default)')),
    ('cmsplugin_zinnia/entry_detail.html', _('Entry detailed')),
    ('cmsplugin_zinnia/entry_slider.html', _('Entry slider'))] \
    + PLUGINS_TEMPLATES


class LatestEntriesPlugin(CMSPlugin):
    """CMS Plugin for displaying latest entries"""

    categories = models.ManyToManyField(
        Category, verbose_name=_('categories'),
        blank=True, null=True)
    subcategories = models.BooleanField(
        _('include subcategories'), default=True,
        help_text=_('include the entries belonging the subcategories'))
    authors = models.ManyToManyField(
        User, verbose_name=_('authors'), blank=True, null=True)
    tags = models.ManyToManyField(
        Tag, verbose_name=_('tags'), blank=True, null=True)

    number_of_entries = models.IntegerField(
        _('number of entries'), default=5,
        help_text=_('0 means all the entries'))
    template_to_render = models.CharField(
        _('template'), blank=True,
        max_length=250, choices=TEMPLATES,
        help_text=_('template used to display the plugin'))

    @property
    def render_template(self):
        """Override render_template to use
        the template_to_render attribute"""
        return self.template_to_render

    def copy_relations(self, old_instance):
        """Duplicate ManyToMany relations on plugin copy"""
        self.tags = old_instance.tags.all()
        self.authors = old_instance.authors.all()
        self.categories = old_instance.categories.all()

    def __unicode__(self):
        return _('%s entries') % self.number_of_entries


class SelectedEntriesPlugin(CMSPlugin):
    """CMS Plugin for displaying custom entries"""

    entries = models.ManyToManyField(
        Entry, verbose_name=_('entries'))
    template_to_render = models.CharField(
        _('template'), blank=True,
        max_length=250, choices=TEMPLATES,
        help_text=_('template used to display the plugin'))

    @property
    def render_template(self):
        """Override render_template to use
        the template_to_render attribute"""
        return self.template_to_render

    def copy_relations(self, old_instance):
        """Duplicate ManyToMany relations on plugin copy"""
        self.entries = old_instance.entries.all()

    def __unicode__(self):
        return _('%s entries') % self.entries.count()


class RandomEntriesPlugin(CMSPlugin):
    """CMS Plugin for displaying random entries"""

    number_of_entries = models.IntegerField(
        _('number of entries'), default=5)
    template_to_render = models.CharField(
        _('template'), blank=True,
        max_length=250, choices=TEMPLATES,
        help_text=_('template used to display the plugin'))

    def __unicode__(self):
        return _('%s entries') % self.number_of_entries


class QueryEntriesPlugin(CMSPlugin):
    """CMS Plugin for displaying entries
    based on a search pattern"""

    query = models.CharField(
        _('query'), max_length=250,
        help_text=_(
            'You can use - to exclude words or phrases, &quot;double '
            'quotes&quot; for exact phrases and the AND/OR boolean '
            'operators combined with parenthesis for complex queries.'))
    number_of_entries = models.IntegerField(
        _('number of entries'), default=5,
        help_text=_('0 means all the entries'))
    template_to_render = models.CharField(
        _('template'), blank=True,
        max_length=250, choices=TEMPLATES,
        help_text=_('template used to display the plugin'))

    @property
    def render_template(self):
        """Override render_template to use
        the template_to_render attribute"""
        return self.template_to_render

    def __unicode__(self):
        return _('%s entries') % self.number_of_entries


class CalendarEntriesPlugin(CMSPlugin):
    """CMS Plugin for displaying a calendar with
    published entries"""

    year = models.IntegerField(_('year'), null=True, blank=True)
    month = models.IntegerField(_('month'), null=True, blank=True)

    def __unicode__(self):
        name = _('Calendar entries')
        if self.year:
            name = '%s: %s/%s' % (name, self.year, self.month)
        return '%s' % name


def invalidate_menu_cache(sender, **kwargs):
    """Signal receiver to invalidate the menu_pool
    cache when an entry is posted"""
    menu_pool.clear()

post_save.connect(
    invalidate_menu_cache, sender=Entry,
    dispatch_uid='zinnia.entry.postsave.invalidate_menu_cache')
post_delete.connect(
    invalidate_menu_cache, sender=Entry,
    dispatch_uid='zinnia.entry.postdelete.invalidate_menu_cache')
