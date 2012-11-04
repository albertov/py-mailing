import json
from pkg_resources import resource_filename

from sqlalchemy.orm.attributes import InstrumentedAttribute
from bottle import Bottle, redirect, abort, response, static_file, request

from ..models import (Mailing, NoResultFound, Item, Category, Recipient, Group,
                      Image, Template, ExternalLink, Article)
from ..html import HTMLPageComposer
from .validators import (validate, ModelListValidator, MailingValidator,
                         CategoryValidator, ItemValidator, InvalidForm)

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
 
def generic_collection_view(model, plural=None, filter=None):
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

def generic_item_view(model, plural=None):
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

def generic_item_delete(model):
    def delete(id, db):
        item = db.query(model).get(id.split('::'))
        db.delete(item)
        db.commit()
        return {
            'success': True,
        }
    return delete



# Mailing views
app.route('/mailing/')(generic_collection_view(Mailing))

@app.route('/mailing/', method='POST')
def new_mailing(db):
    form = validate(MailingValidator, json.load(request.body))
    if not form.is_valid:
        return _invalid_form_response(form)
    ob = Mailing()
    _update_from_form(ob, form)

    if 'xhtml' not in ob.templates:
        ob.templates['xhtml'] = Template.latest_by_type(db, 'xhtml')
    ob.number = ob.next_number(db)
    db.add(ob)
    db.commit()
    mailings = [ob.__json__()]
    return {
        'success': True,
        'mailings': mailings
    }

app.route('/mailing/<id>')(generic_item_view(Mailing))
app.route('/mailing/<id>', method='DELETE')(generic_item_delete(Mailing))

@app.route('/mailing/<id>', method='PUT')
def update_mailing(id, db):
    form = validate(MailingValidator, json.load(request.body))
    if not form.is_valid:
        return _invalid_form_response(form)
    ob = db.query(Mailing).get(id)
    _update_from_form(ob, form)
    mailings = [ob.__json__()]
    db.commit()
    return {
        'success': True,
        'mailings': mailings
    }


# Item views
app.route('/item/')(generic_collection_view(Item))

@app.route('/item/', method='POST')
def new_item(db):
    data = json.load(request.body)
    try:
        if isinstance(data, dict):
            items = [_create_one_item(db, data)]
        else:
            items = [_create_one_item(db, d) for d in data]
    except InvalidForm, e:
       return _invalid_form_response(e.form) 
    db.commit()
    items = [ob.__json__() for ob in items]
    return {
        'success': True,
        'items': items
    }

def _create_one_item(db, data):
    form = validate(ItemValidator, data, raises=True)
    type = form.pop('type')
    cls = globals()[type]
    ob = cls()
    _update_from_form(ob, form)
    db.add(ob)
    return ob

@app.route('/item/<id>', method='PUT')
def update_item(id, db):
    data = json.load(request.body)
    try:
        if isinstance(data, dict):
            ob = db.query(Item).get(id)
            items = [_update_one_item(ob, db, data)]
        else:
            ids = [d['id'] for d in data]
            obs = dict((o.id, o)
                       for o in db.query(Item).filter(Item.id.in_(ids)).all())
            items = [_update_one_item(obs[d['id']], db, d) for d in data]
    except InvalidForm, e:
       return _invalid_form_response(e.form) 
    items = [ob.__json__() for ob in items]
    db.commit()
    return {
        'success': True,
        'items': items
    }

def _update_one_item(ob, db, data):
    form = validate(ItemValidator, data, raises=True)
    type = form.pop('type')
    cls = globals()[type]
    if ob.type != type:
        db.delete(ob)
        db.flush()
        ob = cls(id=ob.id)
        db.add(ob)
    _update_from_form(ob, form)
    return ob

app.route('/item/<id>', method='DELETE')(generic_item_delete(Item))



app.route('/image/')(generic_collection_view(Image))
app.route('/recipient/')(generic_collection_view(Recipient))
app.route('/group/')(generic_collection_view(Group))

app.route('/category/')(
    generic_collection_view(Category, 'categories', Category.category_id==None))
app.route('/category/<id>')(generic_item_view(Category, 'categories'))

@app.route('/category/', method='POST')
def new_category(db):

    form = validate(CategoryValidator, json.load(request.body))
    if not form.is_valid:
        return _invalid_form_response(form)
    ob = Category()
    _update_from_form(ob, form)
    db.add(ob)
    db.commit()
    categories = [ob.__json__()]
    return {
        'success': True,
        'categories': categories
    }

@app.route('/category/<id>', method='PUT')
def update_category(id, db):
    form = validate(CategoryValidator, json.load(request.body))
    if not form.is_valid:
        return _invalid_form_response(form)
    else:
        ob = db.query(Category).get(id)
        _update_from_form(ob, form)
        categories = [ob.__json__()]
        db.commit()
        return {
            'success': True,
            'categories': categories
        }


def _get_composer(db, number):
    try:
        m = Mailing.by_number(db, number, eager=True)
    except NoResultFound:
        abort(404)
    return HTMLPageComposer(m)


def _update_from_form(ob, form):
    cls = ob.__class__
    for key in form:
        new_value = form[key]
        desc = getattr(cls, key, None)
        if isinstance(desc, InstrumentedAttribute):
            old_value = getattr(ob, key, None)
            if old_value != new_value:
                setattr(ob, key, new_value)

@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=resource_filename(__name__, 'static'))
