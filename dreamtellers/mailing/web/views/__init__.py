from pkg_resources import resource_filename

from .. import app
from .base import static_file

def _import_views():
    """Imports all modules in current package"""
    import os.path
    import glob
    views = [os.path.basename(f)[:-3]
             for f in glob.glob(resource_filename(__name__, '*.py'))
             if os.path.basename(f) != '__init__.py']
    __import__(__name__, fromlist=views, level=1) 

_import_views()

@app.route('/admin/', name='admin', template='admin_index.html')
def index():
    return {
        'debug': app.config['debug']
    }

STATIC_ROOT = resource_filename('dreamtellers.mailing.web', 'static')
@app.route('/static/<filename:path>', name='static')
def server_static(filename):
    return static_file(filename, root=STATIC_ROOT)
