"""Placeholder model for Zinnia"""
import inspect

from django.db import models
from django.template.context import RequestContext

from cms.models.fields import PlaceholderField
from cms.plugin_rendering import ContentRenderer

from zinnia.models_bases.entry import AbstractEntry


def render_placeholder(placeholder, request):
    """
    See http://docs.django-cms.org/en/develop/upgrade/3.4.html#manual-plugin-rendering
    """
    renderer = ContentRenderer(request)
    context = RequestContext(request)
    context['request'] = request
    content = renderer.render_placeholder(placeholder, context=context)
    return content


class PlaceholderEntry(models.Model):
    """
    Abstract model class adding a Placeholder to edit content.
    """

    content_placeholder = PlaceholderField('content')

    def acquire_request(self):
        """
        Inspect the stack to acquire the current request used,
        to render the placeholder. I'm really sorry for this,
        but if you have a better way, you are welcome !
        """
        frame = None
        request = None

        try:
            for f in inspect.stack()[1:]:
                frame = f[0]
                args, varargs, keywords, alocals = inspect.getargvalues(frame)
                if not request and 'request' in args:
                    request = alocals['request']
        finally:
            del frame

        return request

    @property
    def html_content(self):
        """
        Render the content_placeholder field dynamicly.
        https://github.com/Fantomas42/cmsplugin-zinnia/issues/3
        """
        request = self.acquire_request()
        try:
            return render_placeholder(self.content_placeholder, request)
        except (AttributeError, KeyError):
            # Should happen when ``context`` and ``request``
            # have not been found in the stack.
            pass
        return self.content  # Ultimate fallback

    class Meta(AbstractEntry.Meta):
        """
        PlaceholderEntry's Meta
        """
        abstract = True


class EntryPlaceholder(PlaceholderEntry,
                       AbstractEntry):
    """
    Entry with a Placeholder to edit content.
    """

    class Meta(AbstractEntry.Meta):
        """
        EntryPlaceholder's Meta
        """
        abstract = True
