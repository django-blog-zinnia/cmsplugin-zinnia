"""Views for the cmsplugin_zinnia demo"""
from django.template import loader
from django.http import HttpResponseServerError

from sekizai.context import SekizaiContext


def server_error(request, template_name='500.html'):
    """
    500 error handler.
    Return a SekizaiContext to avoid another 500 error.
    """
    t = loader.get_template(template_name)
    return HttpResponseServerError(
        t.render(SekizaiContext()))
