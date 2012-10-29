import sys
import os.path
from optparse import OptionParser

from bottle import run
from paste.deploy.converters import asbool

from sqlalchemy import engine_from_config

from . import app
from ..models import metadata

parser = OptionParser()
parser.add_option('-b', '--bind', dest='bind', default='localhost:8080')
parser.add_option('-d', '--db', dest='db', default='~/.mailing.db')

def main(args=None):
    opts = parser.parse_args(args)[0]
    configure_sqlalchemy(app,
        {'sqlalchemy.url': 'sqlite:///'+os.path.expanduser(opts.db)}
        )
    configure_genshi(app, {'genshi.auto_reload':False})
    host, port = opts.bind.split(':')
    run(app, host=host, port=int(port))

def configure_sqlalchemy(app, config, prefix='sqlalchemy.'):
    from bottle.ext.sqlalchemy import Plugin
    plugin = Plugin(
        engine_from_config(config, prefix),
        metadata,
        keyword='db',
        create=True,
        commit=False,
        )
    app.install(plugin)

def configure_genshi(app, config, prefix='genshi.'):
    from .template import Plugin
    pos = len(prefix)
    config = dict((k[pos:], v) for k,v in config.iteritems()
                  if k.startswith(prefix))
    config['auto_reload'] = asbool(config.get('auto_reload',
                                   config.get('debug', False)))
    app.install(Plugin())

    

def app_factory(global_config, **local_config):
    app.catchall = False
    config = dict(global_config, **local_config)
    configure_sqlalchemy(app, config)
    configure_genshi(app, config)
    return app.wsgi

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
