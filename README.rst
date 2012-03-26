================
Cmsplugin-zinnia
================

Cmsplugin-zinnia is a bridge between `django-blog-zinnia`_ and
`django-cms`_.

This package provides plugins, menus and apphook to integrate your Zinnia
powered Weblog into your django-cms Web site.

The code bundled in this application is a copy of the original
``zinnia.plugins`` module, made for forward compatibility with Zinnia
v0.11.

.. contents::

.. _installation:

Installation
============

Once Zinnia and the CMS are installed, you simply have to register
``cmsplugin_zinnia``, in the ``INSTALLED_APPS`` section of your
project's settings.

.. _entry-placeholder:

Entries with plugins
====================

If you want to use the plugin system of django-cms in your entries, an
extended ``Entry`` with a ``PlaceholderField`` is provided in this package.

Just add this line in your project's settings to use it. ::

  ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'

.. _settings:

Settings
========

CMSPLUGIN_ZINNIA_APP_MENUS
--------------------------
**Default value:** ::

  ('cmsplugin_zinnia.menu.EntryMenu',
   'cmsplugin_zinnia.menu.CategoryMenu',
   'cmsplugin_zinnia.menu.TagMenu',
   'cmsplugin_zinnia.menu.AuthorMenu')

List of strings representing the path to the `Menu` class provided by the
Zinnia AppHook.

CMSPLUGIN_ZINNIA_HIDE_ENTRY_MENU
--------------------------------
**Default value:** ``True``

Boolean used for displaying or not the entries in the ``EntryMenu`` object.

CMSPLUGIN_ZINNIA_TEMPLATES
--------------------------
**Default value:** ``()`` (Empty tuple)

List of tuple for extending the plugins rendering templates.


.. _django-blog-zinnia: http://django-blog-zinnia.com/
.. _django-cms: http://django-cms.com/
