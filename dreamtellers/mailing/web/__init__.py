from pkg_resources import resource_filename

from bottle import Bottle, redirect, abort, response, static_file, request

from ..models import (Mailing, NoResultFound, Item, Category, Recipient, Group,
                      Image)
from ..html import HTMLPageComposer
from .validators import validate, ModelListValidator

app = Bottle()


@app.route('/', template='index.html')
def index():
    return {}

@app.route('/mailing/<number:int>/')
def mailing(number, db):
    return _get_composer(db, number).get_file('index.html').data

 
def list_view(model, plural=None):
    if plural is None:
        plural = model.__name__.lower()+'s'
    def view(db):
        form = validate(ModelListValidator(model), request.params)
        if not form.is_valid:
            response.status = '400 Bad Request'
            return {
                'success':False,
                'message': form.message,
                'errors': form.errors,
            }
        else:
            query = db.query(model)
            if form['filter']:
                for f in form['filter']:
                    query = query.filter(f)
            total = query.count()
            query = query.limit(form['limit']).offset(form['start'])
            if form['sort']:
                query = query.order_by(*form['sort'])
            return {
                'success': True,
                'total': total,
                 plural: [m.__json__() for m in query]
            }
    view.func_name = 'list_'+plural
    return view

app.route('/mailing/')(list_view(Mailing))
app.route('/item/')(list_view(Item))
app.route('/image/')(list_view(Image))
app.route('/recipient/')(list_view(Recipient))
app.route('/group/')(list_view(Group))
app.route('/category/')(list_view(Category, 'categories'))

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
