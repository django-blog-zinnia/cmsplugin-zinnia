"""Models of Zinnia CMS Plugins"""
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from cms.models.pluginmodel import CMSPlugin

from cmsplugin_zinnia.settings import PLUGINS_TEMPLATES

TEMPLATES = [
    ('cmsplugin_zinnia/entry_list.html', _('Entry list (default)')),
    ('cmsplugin_zinnia/entry_detail.html', _('Entry detailed')),
    ('cmsplugin_zinnia/entry_slider.html', _('Entry slider'))] \
    + PLUGINS_TEMPLATES


@python_2_unicode_compatible
class LatestEntriesPlugin(CMSPlugin):
    """
    CMS Plugin for displaying latest entries
    """

    featured = models.NullBooleanField(
        _('featured'),
        blank=True, null=True,
        choices=((True, _('Show featured entries only')),
                 (False, _('Hide featured entries'))))
    categories = models.ManyToManyField(
        'zinnia.Category', verbose_name=_('categories'),
        blank=True)
    subcategories = models.BooleanField(
        _('include subcategories'), default=True,
        help_text=_('include the entries belonging the subcategories'))
    authors = models.ManyToManyField(
        'zinnia.Author', verbose_name=_('authors'),
        blank=True)
    tags = models.ManyToManyField(
        'tagging.Tag', verbose_name=_('tags'),
        blank=True)

    number_of_entries = models.PositiveIntegerField(
        _('number of entries'), default=5,
        help_text=_('0 means all the entries'))
    offset = models.PositiveIntegerField(
        _('offset'), default=0,
        help_text=_('number of entries to skip from top of list'))
    template_to_render = models.CharField(
        _('template'), blank=True,
        max_length=250, choices=TEMPLATES,
        help_text=_('template used to display the plugin'))

    @property
    def render_template(self):
        """
        Override render_template to use
        the template_to_render attribute
        """
        return self.template_to_render

    def copy_relations(self, old_instance):
        """
        Duplicate ManyToMany relations on plugin copy
        """
        self.tags = old_instance.tags.all()
        self.authors = old_instance.authors.all()
        self.categories = old_instance.categories.all()

    def __str__(self):
        return _('%s entries') % self.number_of_entries


@python_2_unicode_compatible
class SelectedEntriesPlugin(CMSPlugin):
    """
    CMS Plugin for displaying custom entries
    """

    entries = models.ManyToManyField(
        'zinnia.Entry', verbose_name=_('entries'))
    template_to_render = models.CharField(
        _('template'), blank=True,
        max_length=250, choices=TEMPLATES,
        help_text=_('template used to display the plugin'))

    @property
    def render_template(self):
        """
        Override render_template to use
        the template_to_render attribute
        """
        return self.template_to_render

    def copy_relations(self, old_instance):
        """
        Duplicate ManyToMany relations on plugin copy
        """
        self.entries = old_instance.entries.all()

    def __str__(self):
        return _('%s entries') % self.entries.count()


@python_2_unicode_compatible
class RandomEntriesPlugin(CMSPlugin):
    """
    CMS Plugin for displaying random entries
    """

    number_of_entries = models.PositiveIntegerField(
        _('number of entries'), default=5)
    template_to_render = models.CharField(
        _('template'), blank=True,
        max_length=250, choices=TEMPLATES,
        help_text=_('template used to display the plugin'))

    def __str__(self):
        return _('%s entries') % self.number_of_entries


@python_2_unicode_compatible
class QueryEntriesPlugin(CMSPlugin):
    """
    CMS Plugin for displaying entries
    based on a search pattern
    """

    query = models.CharField(
        _('query'), max_length=250,
        help_text=_(
            'You can use - to exclude words or phrases, &quot;double '
            'quotes&quot; for exact phrases and the AND/OR boolean '
            'operators combined with parenthesis for complex queries.'))
    number_of_entries = models.PositiveIntegerField(
        _('number of entries'), default=5,
        help_text=_('0 means all the entries'))
    template_to_render = models.CharField(
        _('template'), blank=True,
        max_length=250, choices=TEMPLATES,
        help_text=_('template used to display the plugin'))

    @property
    def render_template(self):
        """
        Override render_template to use
        the template_to_render attribute
        """
        return self.template_to_render

    def __str__(self):
        return _('%s entries') % self.number_of_entries


@python_2_unicode_compatible
class CalendarEntriesPlugin(CMSPlugin):
    """
    CMS Plugin for displaying a calendar with
    published entries
    """

    year = models.PositiveIntegerField(_('year'), null=True, blank=True)
    month = models.PositiveIntegerField(_('month'), null=True, blank=True)

    def __str__(self):
        name = six.text_type(_('Calendar entries'))
        if self.year:
            name = '%s: %s/%s' % (name, self.year, self.month)
        return name
