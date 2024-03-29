import sys
import os.path
from optparse import OptionParser

from bottle import Bottle, request
from paste.deploy.converters import asbool
from sqlalchemy import engine_from_config

from .models import Plugin as SAPlugin, Config
from .template import Plugin as GenshiPlugin


app = Bottle()

from . import views

def static_url(s):
    return app.get_url('static', filename=s)

def get_url(*args, **kw):
    faked_environ = False
    if not hasattr(request, 'environ'):
        faked_environ = True
        script_name = Config.setdefault('server.script_name', '')
        request.environ = {'SCRIPT_NAME': script_name}
    try:
        return app.get_url(*args, **kw)
    finally:
        if faked_environ:
            del request.environ
    

def configure_sqlalchemy(app, config, prefix='sqlalchemy.'):
    if 'engine' in config:
        engine = config['engine']
    else:
        engine = engine_from_config(config, prefix)
    plugin = SAPlugin(engine)
    app.install(plugin)

def configure_genshi(app, config, prefix='genshi.'):
    pos = len(prefix)
    config = dict((k[pos:], v) for k,v in config.iteritems()
                  if k.startswith(prefix))
    config['auto_reload'] = asbool(config.get('auto_reload',
                                   config.get('debug', False)))
    app.install(GenshiPlugin())

    

def app_factory(global_config, **local_config):
    app.catchall = False
    config = dict(global_config, **local_config)
    config['debug'] = asbool(config.get('debug', False))
    app.config = config
    configure_sqlalchemy(app, config)
    configure_genshi(app, config)
    return app


parser = OptionParser()
parser.add_option('-b', '--bind', dest='bind', default='localhost:8080')
parser.add_option('-d', '--db', dest='db', default='~/.mailing.db')
parser.add_option('', '--debug', dest='debug', action='store_true')

def main(args=None):
    from paste.httpserver import serve
    opts = parser.parse_args(args)[0]
    app = app_factory({
        'sqlalchemy.url': 'sqlite:///'+os.path.expanduser(opts.db),
        'genshi.auto_reload': opts.debug,
        'debug': opts.debug
    })
    host, port = opts.bind.split(':')
    serve(app, host=host, port=int(port), use_threadpool=True)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
