from bottle import request
from genshi.template import TemplateLoader
from pkg_resources import resource_filename


class Plugin(object):
    name = 'genshi'
    api = 2

    def __init__(self, auto_reload=True):
        self.loader = TemplateLoader([resource_filename(__name__, 'templates')],
                                     auto_reload=auto_reload)
        from bottle import request
        from . import static_url
        from .models import Config
        self.global_variables = dict(
            static_url = static_url,
            request = request,
            Config = Config,
            )

    def setup(self, app):
        pass

    def apply(self, callback, route):
        template_name = route.config.get('template')
        serializer = route.config.get('serializer', 'xhtml')
        if template_name is None:
            return callback
        else:
            def wrapper(*args, **kw):
                namespace = callback(*args, **kw)
                namespace.update(self.global_variables)
                template = self.loader.load(template_name)
                return template.generate(**namespace).render(serializer)
            return wrapper


    def close(self):
        pass