from pkg_resources import resource_filename

from bottle import Bottle, redirect, abort, response, static_file, request

from ..models import Mailing, NoResultFound
from ..html import HTMLPageComposer
from .validators import validate, ModelListValidator

app = Bottle()


@app.route('/', template='index.html')
def index():
    return {}

@app.route('/mailing/<number:int>/')
def mailing(number, db):
    return _get_composer(db, number).get_file('index.html').data

@app.route('/mailing/')
def mailings(db):
    form = validate(ModelListValidator(Mailing), request.params)
    if not form.is_valid:
        response.status = '400 Bad Request'
        return {
            'success':False,
            'message': form.message,
            'errors': form.errors,
        }
    else:
        query = db.query(Mailing)
        total = query.count()
        if form['sort']:
            query = query.order_by(*form['sort'])
        query = query.limit(form['limit']).offset(form['start'])
        return {
            'success': True,
            'total': total,
            'mailings': [
                dict(number=m.number,
                     date=m.date.isoformat() if m.date else None)
                for m in query
            ]
        }

@app.route('/mailing/<number:int>/<filename:re:.+>')
def mailing_file(number, filename, db):
    f = _get_composer(db, number).get_file(filename)
    response.content_type = f.content_type
    return f.data

def _get_composer(db, number):
    try:
        m = db.query(Mailing).filter_by(number=number).one()
    except NoResultFound:
        abort(404)
    return HTMLPageComposer(m)

@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=resource_filename(__name__, 'static'))
