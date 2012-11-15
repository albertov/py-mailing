from pkg_resources import resource_filename

from ...util import import_all_modules_from_package
from .. import app
from .base import static_file

import_all_modules_from_package(__name__)

@app.route('/admin/', name='admin', template='admin_index.html')
def index():
    return {
        'debug': app.config['debug']
    }

STATIC_ROOT = resource_filename('dreamtellers.mailing.web', 'static')
@app.route('/static/<filename:path>', name='static')
def server_static(filename):
    return static_file(filename, root=STATIC_ROOT)
