"""Applications hooks for cmsplugin_zinnia"""
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from cmsplugin_zinnia.settings import APP_MENUS


class ZinniaApphook(CMSApp):
    """Zinnia's Apphook"""
    name = _('Zinnia Weblog')
    urls = ['zinnia.urls']
    menus = APP_MENUS

apphook_pool.register(ZinniaApphook)
