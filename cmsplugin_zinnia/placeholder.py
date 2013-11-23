"""Placeholder model for Zinnia"""
import inspect

from django.template.context import Context, RequestContext
from cms.models.fields import PlaceholderField
from cms.plugin_rendering import render_placeholder

from zinnia.models_bases.entry import AbstractEntry


class EntryPlaceholder(AbstractEntry):
    """Entry with a Placeholder to edit content"""

    content_placeholder = PlaceholderField('content')

    def acquire_context(self):
        """
        Inspect the stack to acquire the current context used,
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
                if 'context' in args:
                    return alocals['context']
        finally:
            del frame
        
        if request is not None:
            return RequestContext(request)
        else:
            return Context()
        

    @property
    def html_content(self):
        """
        Render the content_placeholder field dynamicly.
        https://github.com/Fantomas42/cmsplugin-zinnia/issues/3
        """
        context = self.acquire_context()
        return render_placeholder(self.content_placeholder, context)

    class Meta(AbstractEntry.Meta):
        """EntryPlaceholder's Meta"""
        abstract = True
