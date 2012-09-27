import json
from pkg_resources import resource_filename

from bottle import Bottle, redirect, abort, response, static_file, request

from ..models import (Mailing, NoResultFound, Item, Category, Recipient, Group,
                      Image, Template)
from ..html import HTMLPageComposer
from .validators import (validate, ModelListValidator, MailingValidator,
                         CategoryValidator)

app = Bottle()


@app.route('/', template='index.html')
def index():
    return {}

@app.route('/m/<number:int>/')
def mailing(number, db):
    return _get_composer(db, number).get_file('index.html').data

@app.route('/m/<number:int>/<filename:re:.+>')
def mailing_file(number, filename, db):
    f = _get_composer(db, number).get_file(filename)
    response.content_type = f.content_type
    return f.data


def _invalid_form_response(form):
    response.status = '400 Bad Request'
    return {
        'success':False,
        'message': form.message,
        'errors': form.errors,
    }
 
def collection_view(model, plural=None, filter=None):
    if plural is None:
        plural = model.__name__.lower()+'s'
    def view(db):
        form = validate(ModelListValidator(model), request.params)
        if not form.is_valid:
            return _invalid_form_response(form)
        else:
            query = db.query(model)
            if filter is not None:
                query = query.filter(filter)
            if form['sort']:
                query = query.order_by(*form['sort'])
            if form['filter']:
                for f in form['filter']:
                    query = query.filter(f)
            total = query.count()
            query = query.limit(form['limit']).offset(form['start'])
            return {
                'success': True,
                'total': total,
                 plural: [m.__json__() for m in query]
            }
    view.func_name = 'list_'+plural
    return view

def item_view(model, plural=None):
    if plural is None:
        plural = model.__name__.lower()+'s'
    def view(id, db):
        item = db.query(model).get(id.split('::'))
        return {
            'success': True,
            'total': 1,
             plural: [item.__json__()]
        }
    return view

def item_delete(model):
    def delete(id, db):
        item = db.query(model).get(id.split('::'))
        db.delete(item)
        db.commit()
        return {
            'success': True,
        }
    return delete

app.route('/mailing/')(collection_view(Mailing))

@app.route('/mailing/', method='POST')
def new_mailing(db):
    form = validate(MailingValidator, json.load(request.body))
    if not form.is_valid:
        return _invalid_form_response(form)
    ob = Mailing()
    for key in form:
        setattr(ob, key, form[key])

    if 'xhtml' not in ob.templates:
        ob.templates['xhtml'] = Template.latest_by_type(db, 'xhtml')
    ob.number = ob.next_number(db)
    db.add(ob)
    db.commit()
    return {
        'success': True,
        'mailings': [ob.__json__()]
    }

app.route('/mailing/<id>')(item_view(Mailing))
app.route('/mailing/<id>', method='DELETE')(item_delete(Mailing))

@app.route('/mailing/<id>', method='PUT')
def update_mailing(id, db):
    form = validate(MailingValidator, json.load(request.body))
    if not form.is_valid:
        return _invalid_form_response(form)
    ob = db.query(Mailing).get(id)
    for key in form:
        setattr(ob, key, form[key])
    db.commit()
    return {
        'success': True,
        'mailings': [ob.__json__()]
    }

app.route('/item/')(collection_view(Item))
app.route('/image/')(collection_view(Image))
app.route('/recipient/')(collection_view(Recipient))
app.route('/group/')(collection_view(Group))

app.route('/category/')(
    collection_view(Category, 'categories', Category.category_id==None))
app.route('/category/<id>')(item_view(Category, 'categories'))

@app.route('/category/', method='POST')
def new_category(db):
    form = validate(CategoryValidator, json.load(request.body))
    if not form.is_valid:
        return _invalid_form_response(form)
    ob = Category()
    for key in form:
        setattr(ob, key, form[key])
    db.add(ob)
    db.commit()
    return {
        'success': True,
        'categories': [ob.__json__()]
    }

@app.route('/category/<id>', method='PUT')
def update_categroy(id, db):
    form = validate(CategoryValidator, json.load(request.body))
    if not form.is_valid:
        return _invalid_form_response(form)
    else:
        ob = db.query(Category).get(id)
        for key in form:
            setattr(ob, key, form[key])
        db.commit()
        return {
            'success': True,
            'categories': [ob.__json__()]
        }


def _get_composer(db, number):
    try:
        m = db.query(Mailing).filter_by(number=number).one()
    except NoResultFound:
        abort(404)
    return HTMLPageComposer(m)

@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=resource_filename(__name__, 'static'))
