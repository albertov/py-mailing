import sys
import os.path
from optparse import OptionParser

from bottle import run

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
    host, port = opts.bind.split(':')
    run(app, host=host, port=int(port))

def configure_sqlalchemy(app, config):
    from bottle.ext.sqlalchemy import Plugin
    plugin = Plugin(
        engine_from_config(config),
        metadata,
        keyword='db',
        create=True,
        commit=False,
        )
    app.install(plugin)
    from .template import Plugin
    app.install(Plugin())

    

def app_factory(global_config, **local_config):
    app.catchall = False
    config = dict(global_config, **local_config)
    configure_sqlalchemy(app, config)
    return app.wsgi

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
