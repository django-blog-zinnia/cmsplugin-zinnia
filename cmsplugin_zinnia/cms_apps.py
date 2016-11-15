"""Application hooks for cmsplugin_zinnia"""
import warnings

from importlib import import_module
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from cmsplugin_zinnia.settings import APP_URLS
from cmsplugin_zinnia.settings import APP_MENUS

app_menus = []
for menu_string in APP_MENUS:
    try:
        dot = menu_string.rindex('.')
        menu_module = menu_string[:dot]
        menu_name = menu_string[dot + 1:]
        app_menus.append(getattr(import_module(menu_module), menu_name))
    except (ImportError, AttributeError):
        warnings.warn('%s menu cannot be imported' % menu_string,
                      RuntimeWarning)


class ZinniaApphook(CMSApp):
    """
    Zinnia's Apphook
    """
    name = _('Zinnia Weblog')
    app_name = 'zinnia'

    def get_urls(self, page=None, language=None, **kwargs):
        return APP_URLS

    def get_menus(self, page=None, language=None, **kwargs):
        return app_menus


apphook_pool.register(ZinniaApphook)
