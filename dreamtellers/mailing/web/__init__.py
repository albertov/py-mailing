from bottle import Bottle, redirect, abort, response

from ..models import Mailing, NoResultFound
from ..html import HTMLPageComposer


app = Bottle()


@app.route('/')
def index():
    return "hola"

@app.route('/mailing/<number:int>/')
def mailing(number, db):
    return _get_composer(db, number).get_file_data('index.html')

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
