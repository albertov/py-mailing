from pkg_resources import resource_filename
from .. import app
from .base import static_file
from . import mailings, items, category, group, recipient

@app.route('/', template='index.html')
def index():
    return {}

# Static view
STATIC_ROOT = resource_filename('dreamtellers.mailing.web', 'static')
@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=STATIC_ROOT)
