"""Settings of cmsplugin_zinnia"""
from django.conf import settings

HIDE_ENTRY_MENU = getattr(settings, 'CMSPLUGIN_ZINNIA_HIDE_ENTRY_MENU', True)

PLUGINS_TEMPLATES = getattr(settings, 'CMSPLUGIN_ZINNIA_TEMPLATES', [])

APP_URLS = getattr(settings, 'CMSPLUGIN_ZINNIA_APP_URLS', ['zinnia.urls'])

APP_MENUS = getattr(settings, 'CMSPLUGIN_ZINNIA_APP_MENUS',
                    ['cmsplugin_zinnia.menu.EntryMenu',
                     'cmsplugin_zinnia.menu.CategoryMenu',
                     'cmsplugin_zinnia.menu.TagMenu',
                     'cmsplugin_zinnia.menu.AuthorMenu'])
