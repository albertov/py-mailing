import json

from ..models import Config, Session

from .. import app
from .base import request, error_response

@app.get('/config')
def get_config():
    return Config.__json__()

@app.put('/config')
def update_config():
    try:
        data = json.load(request.body)
    except ValueError:
        return error_response('Invalid JSON data')
    Config.update((str(k), v) for k,v in data.iteritems())
    Session.commit()
    return {
        'success': True,
        'config': Config.__json__()
    }
