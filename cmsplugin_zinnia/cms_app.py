"""Applications hooks for cmsplugin_zinnia"""
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from cmsplugin_zinnia.settings import APP_MENUS, APP_URLS


class ZinniaApphook(CMSApp):
    """Zinnia's Apphook"""
    name = _('Zinnia Weblog')
    urls = APP_URLS 
    menus = APP_MENUS

apphook_pool.register(ZinniaApphook)
