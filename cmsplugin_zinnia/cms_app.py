"""Application hooks for cmsplugin_zinnia"""
import warnings

from django.utils.importlib import import_module
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
    urls = APP_URLS
    menus = app_menus
    app_name = 'zinnia'

apphook_pool.register(ZinniaApphook)
