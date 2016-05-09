# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from cmsplugin_zinnia.settings import PLUGINS_TEMPLATES


class Migration(migrations.Migration):

    dependencies = [
        ('zinnia', '0001_initial'),
        ('cms', '__first__'),
        ('tagging', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEntriesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('year', models.PositiveIntegerField(null=True, verbose_name='year', blank=True)),
                ('month', models.PositiveIntegerField(null=True, verbose_name='month', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='LatestEntriesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('featured', models.NullBooleanField(verbose_name='featured', choices=[(True, 'Show featured entries only'), (False, 'Hide featured entries')])),
                ('subcategories', models.BooleanField(default=True, help_text='include the entries belonging the subcategories', verbose_name='include subcategories')),
                ('number_of_entries', models.PositiveIntegerField(default=5, help_text='0 means all the entries', verbose_name='number of entries')),
                ('offset', models.PositiveIntegerField(default=0, help_text='number of entries to skip from top of list', verbose_name='offset')),
                ('template_to_render', models.CharField(blank=True, help_text='template used to display the plugin', max_length=250, verbose_name='template', choices=[(b'cmsplugin_zinnia/entry_list.html', 'Entry list (default)'), (b'cmsplugin_zinnia/entry_detail.html', 'Entry detailed'), (b'cmsplugin_zinnia/entry_slider.html', 'Entry slider')] + PLUGINS_TEMPLATES)),
                ('authors', models.ManyToManyField(to='zinnia.Author', verbose_name='authors', blank=True)),
                ('categories', models.ManyToManyField(to='zinnia.Category', verbose_name='categories', blank=True)),
                ('tags', models.ManyToManyField(to='tagging.Tag', verbose_name='tags', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='QueryEntriesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('query', models.CharField(help_text='You can use - to exclude words or phrases, &quot;double quotes&quot; for exact phrases and the AND/OR boolean operators combined with parenthesis for complex queries.', max_length=250, verbose_name='query')),
                ('number_of_entries', models.PositiveIntegerField(default=5, help_text='0 means all the entries', verbose_name='number of entries')),
                ('template_to_render', models.CharField(blank=True, help_text='template used to display the plugin', max_length=250, verbose_name='template', choices=[(b'cmsplugin_zinnia/entry_list.html', 'Entry list (default)'), (b'cmsplugin_zinnia/entry_detail.html', 'Entry detailed'), (b'cmsplugin_zinnia/entry_slider.html', 'Entry slider')] + PLUGINS_TEMPLATES)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='RandomEntriesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('number_of_entries', models.PositiveIntegerField(default=5, verbose_name='number of entries')),
                ('template_to_render', models.CharField(blank=True, help_text='template used to display the plugin', max_length=250, verbose_name='template', choices=[(b'cmsplugin_zinnia/entry_list.html', 'Entry list (default)'), (b'cmsplugin_zinnia/entry_detail.html', 'Entry detailed'), (b'cmsplugin_zinnia/entry_slider.html', 'Entry slider')] + PLUGINS_TEMPLATES)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='SelectedEntriesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('template_to_render', models.CharField(blank=True, help_text='template used to display the plugin', max_length=250, verbose_name='template', choices=[(b'cmsplugin_zinnia/entry_list.html', 'Entry list (default)'), (b'cmsplugin_zinnia/entry_detail.html', 'Entry detailed'), (b'cmsplugin_zinnia/entry_slider.html', 'Entry slider')] + PLUGINS_TEMPLATES)),
                ('entries', models.ManyToManyField(to='zinnia.Entry', verbose_name='entries')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
