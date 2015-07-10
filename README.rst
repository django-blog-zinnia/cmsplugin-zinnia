================
Cmsplugin-zinnia
================

Cmsplugin-zinnia is a bridge between `django-blog-zinnia`_ and
`django-cms`_.

This package provides plugins, menus and apphook to integrate your Zinnia
powered Weblog into your django-cms Web site.

The code bundled in this application is a copy of the original
``zinnia.plugins`` module, made for forward compatibility with
django-blog-zinnia > 0.11.

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

.. note::
   If you are using South for migrating your models, you have to keep in
   mind that the default migrations bundled with Zinnia do not reflect
   the addition made by the ``EntryPlaceholder`` model.

   A solution to initialize correctly the database can be: ::

     $ python manage.py syncdb --all
     $ python manage.py migrate --fake

Tips for using the apphook
==========================

If you want to use the apphook to provide the blog functionnalities under a
specific URL handled by the CMS, remember this tip:

* Once the apphook is registered, you can remove the inclusion of
  ``'zinnia.urls'`` in ``urls.py`` and then restart the server to see it in
  full effect.

.. _settings:

Settings
========

CMSPLUGIN_ZINNIA_APP_URLS
-------------------------
**Default value:** ``['zinnia.urls']``

The URLsets used for by the Zinnia AppHook.

CMSPLUGIN_ZINNIA_APP_MENUS
--------------------------
**Default value:** ::

  ['cmsplugin_zinnia.menu.EntryMenu',
   'cmsplugin_zinnia.menu.CategoryMenu',
   'cmsplugin_zinnia.menu.TagMenu',
   'cmsplugin_zinnia.menu.AuthorMenu']

List of strings representing the path to the `Menu` class provided by the
Zinnia AppHook.

CMSPLUGIN_ZINNIA_HIDE_ENTRY_MENU
--------------------------------
**Default value:** ``True``

Boolean used for displaying or not the entries in the ``EntryMenu`` object.

CMSPLUGIN_ZINNIA_TEMPLATES
--------------------------
**Default value:** ``[]`` (Empty list)

List of tuple for extending the plugins rendering templates.

Example: ::

  CMSPLUGIN_ZINNIA_TEMPLATES = [
    ('entry_custom.html', 'Entry custom'),
    ('entry_custom_bis.html', 'Entry custom bis')
    ]

.. _changelog:

Changelog
=========

0.8
---

- Compatibility with Django 1.8

0.7
---

- PlaceholderEntry mixin
- Compatibility with Django 1.7 and Zinnia 0.15

0.6
---

- Compatibility with Django-CMS 3.0

0.5.1
-----

- Python 3 compatibility fix
- Better help texts and legends

0.5
---

- Archives plugin
- Tag cloud plugin
- Author list plugin
- Categories plugins
- Featured entries filter
- Offset for latest entries
- Documentation improvements
- Configurable apphook's urls
- Support custom auth.User model
- Fix translations of the plugins
- Fix HTML rendering without context
- Compatibility with Django v1.5
- Compatibility with Zinnia v0.13
- Updating the buildout installation

0.4.1
-----

- Compatibility fix for Django-CMS 2.2+

0.4
---

- Fix issues with Entry.content rendering.
- Compatibility with latest version of Zinnia.

0.3
---

- Calendar plugin.
- QueryEntries plugin.
- Slider template for plugins.
- Documentation improvements.
- Fix breadcrumbs with month abbrev.
- Compatibility with Django 1.4 and Django-CMS 2.3.

0.2
---

- Better demo.
- Renaming modules.
- Fix dependancies with mptt.
- Fix ``EntryPlaceholder``'s Meta.
- ``0`` means all the entries on plugins.
- Set menu Nodes to invisible instead of removing.

0.1
---

- Initial release based on ``zinnia.plugins``.


.. _django-blog-zinnia: http://django-blog-zinnia.com/
.. _django-cms: http://django-cms.com/
