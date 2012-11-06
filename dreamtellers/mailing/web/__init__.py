import json
from pkg_resources import resource_filename

from sqlalchemy.orm.attributes import InstrumentedAttribute
from bottle import Bottle, redirect, abort, response, static_file, request

from ..models import (Session, Mailing, NoResultFound, Item, Category,
                      Recipient, Group, Image, Template, ExternalLink, Article)
from ..html import HTMLPageComposer
from .validators import (validate, ModelListValidator, MailingValidator,
                         CategoryValidator, ItemValidator, InvalidForm)

app = Bottle()


@app.route('/', template='index.html')
def index():
    return {}

# Generic views

_ = lambda s: s
 
def generic_collection_view(model, plural=None, filter=None):
    if plural is None:
        plural = model.__name__.lower()+'s'
    def view():
        form = validate(ModelListValidator(model), request.params)
        if not form.is_valid:
            return _invalid_form_response(form)
        else:
            query = model.query
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
    def view(id):
        item = model.query.get(id.split('::'))
        return {
            'success': True,
            'total': 1,
             plural: [item.__json__()]
        }
    return view

def generic_item_delete(model):
    def delete(id):
        item = model.query.get(id.split('::'))
        if item is not None:
            Session.delete(item)
            Session.commit()
        return {
            'success': True,
        }
    return delete



# Mailing views

@app.route('/m/<number:int>/')
def mailing_by_number(number):
    return _get_composer(number).get_file('index.html').data

@app.route('/m/<number:int>/<filename:re:.+>')
def mailing_file(number, filename):
    f = _get_composer(number).get_file(filename)
    response.content_type = f.content_type
    return f.data

def _get_composer(number):
    try:
        m = Mailing.by_number(number, eager=True)
    except NoResultFound:
        abort(404)
    return HTMLPageComposer(m)


app.route('/mailing/')(generic_collection_view(Mailing))
app.route('/mailing/<id>')(generic_item_view(Mailing))
app.route('/mailing/<id>', method='DELETE')(generic_item_delete(Mailing))


@app.route('/mailing/', method='POST')
def new_mailing():
    form = validate(MailingValidator, request.body)
    if not form.is_valid:
        return _invalid_form_response(form)
    ob = Mailing()
    _update_from_form(ob, form)

    if 'xhtml' not in ob.templates:
        tpl = Template.latest_by_type('xhtml')
        if tpl is not None:
            ob.templates['xhtml'] = tpl
        else:
            return _error_response(
                _('Could not assign a default xhtml template. Please create one first'))
    ob.number = ob.next_number()
    Session.add(ob)
    Session.commit()
    mailings = [ob.__json__()]
    return {
        'success': True,
        'mailings': mailings
    }

@app.route('/mailing/<id>', method='PUT')
def update_mailing(id):
    form = validate(MailingValidator, request.body)
    if not form.is_valid:
        return _invalid_form_response(form)
    ob = Mailing.query.get(id)
    _update_from_form(ob, form)
    mailings = [ob.__json__()]
    Session.commit()
    return {
        'success': True,
        'mailings': mailings
    }


# Item views
app.route('/item/')(generic_collection_view(Item))
app.route('/item/<id>')(generic_item_view(Item))
app.route('/item/<id>', method='DELETE')(generic_item_delete(Item))

@app.route('/item/', method='POST')
def new_item():
    try:
        data = json.load(request.body)
    except ValueError:
        return _error_response('Invalid JSON data')
    try:
        if isinstance(data, dict):
            items = [_create_one_item(data)]
        else:
            items = [_create_one_item(d) for d in data]
    except InvalidForm, e:
       return _invalid_form_response(e.form) 
    Session.commit()
    items = [ob.__json__() for ob in items]
    return {
        'success': True,
        'items': items
    }

def _create_one_item(data):
    form = validate(ItemValidator, data, raises=True)
    type = form.pop('type')
    cls = globals()[type]
    ob = cls()
    _update_from_form(ob, form)
    Session.add(ob)
    return ob

@app.route('/item/<id>', method='PUT')
def update_item(id):
    try:
        data = json.load(request.body)
    except ValueError:
        return _error_response('Invalid JSON data')
    try:
        if isinstance(data, dict):
            ob = Item.query.get(id)
            items = [_update_one_item(ob, data)]
        else:
            ids = [d['id'] for d in data]
            obs = dict((o.id, o)
                       for o in Item.query.filter(Item.id.in_(ids)).all())
            items = [_update_one_item(obs[d['id']], d) for d in data]
    except InvalidForm, e:
       return _invalid_form_response(e.form) 
    items = [ob.__json__() for ob in items]
    Session.commit()
    return {
        'success': True,
        'items': items
    }

def _update_one_item(ob, data):
    form = validate(ItemValidator, data, raises=True)
    type = form.pop('type')
    cls = globals()[type]
    if ob.type != type:
        Session.delete(ob)
        Session.flush()
        ob = cls(id=ob.id)
        Session.add(ob)
    _update_from_form(ob, form)
    return ob



# Category views

app.route('/category/')(
    generic_collection_view(Category, 'categories', Category.category_id==None))
app.route('/category/<id>')(generic_item_view(Category, 'categories'))
app.route('/category/<id>', method='DELETE')(generic_item_delete(Category))


@app.route('/category/', method='POST')
def new_category():

    form = validate(CategoryValidator, request.body)
    if not form.is_valid:
        return _invalid_form_response(form)
    ob = Category()
    _update_from_form(ob, form)
    Session.add(ob)
    Session.commit()
    categories = [ob.__json__()]
    return {
        'success': True,
        'categories': categories
    }

@app.route('/category/<id>', method='PUT')
def update_category(id):
    form = validate(CategoryValidator, request.body)
    if not form.is_valid:
        return _invalid_form_response(form)
    else:
        ob = Category.query.get(id)
        _update_from_form(ob, form)
        categories = [ob.__json__()]
        Session.commit()
        return {
            'success': True,
            'categories': categories
        }


# Recipient views

app.route('/recipient/')(generic_collection_view(Recipient))
app.route('/recipient/<id>')(generic_item_view(Recipient, 'recipients'))
app.route('/recipient/<id>', method='DELETE')(generic_item_delete(Recipient))

# Static view

@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=resource_filename(__name__, 'static'))



# Utilities

def _invalid_form_response(form):
    return _error_response(form.message, form.errors)

def _error_response(message, errors=None):
    response.status = '400 Bad Request'
    return {
        'success':False,
        'message': message,
        'errors': errors,
    }




def _update_from_form(ob, form):
    cls = ob.__class__
    for key in form:
        new_value = form[key]
        desc = getattr(cls, key, None)
        if isinstance(desc, InstrumentedAttribute):
            old_value = getattr(ob, key, None)
            if old_value != new_value:
                setattr(ob, key, new_value)
