"""Settings of cmsplugin_zinnia"""
import warnings

from django.conf import settings
from django.utils.importlib import import_module


HIDE_ENTRY_MENU = getattr(settings, 'CMSPLUGIN_ZINNIA_HIDE_ENTRY_MENU', True)

PLUGINS_TEMPLATES = getattr(settings, 'CMSPLUGIN_ZINNIA_TEMPLATES', [])


APP_MENUS = []
DEFAULT_APP_MENUS = ['cmsplugin_zinnia.menu.EntryMenu',
                     'cmsplugin_zinnia.menu.CategoryMenu',
                     'cmsplugin_zinnia.menu.TagMenu',
                     'cmsplugin_zinnia.menu.AuthorMenu']

for menu_string in getattr(settings, 'CMSPLUGIN_ZINNIA_APP_MENUS',
                           DEFAULT_APP_MENUS):
    try:
        dot = menu_string.rindex('.')
        menu_module = menu_string[:dot]
        menu_name = menu_string[dot + 1:]
        APP_MENUS.append(getattr(import_module(menu_module), menu_name))
    except (ImportError, AttributeError):
        warnings.warn('%s menu cannot be imported' % menu_string,
                      RuntimeWarning)
