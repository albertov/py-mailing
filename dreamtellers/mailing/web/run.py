import sys
import os.path
from optparse import OptionParser

from bottle import run

from sqlalchemy import create_engine

from . import app
from ..models import metadata

parser = OptionParser()
parser.add_option('-b', '--bind', dest='bind', default='localhost')
parser.add_option('-d', '--db', dest='db', default='~/.mailing.db')

def main(args):
    opts = parser.parse_args(args)[0]
    configure_sqlalchemy(app, dbfile=os.path.expanduser(opts.db))
    run(app, host='0.0.0.0', port=8080)

def configure_sqlalchemy(app, dbfile):
    from bottle.ext.sqlalchemy import Plugin
    plugin = Plugin(
        create_engine('sqlite:///'+dbfile, echo=True),
        metadata,
        keyword='db',
        create=True,
        commit=False,
        )
    app.install(plugin)

    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
