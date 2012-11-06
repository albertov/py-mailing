import json
from pkg_resources import resource_filename

from sqlalchemy.orm.attributes import InstrumentedAttribute
from bottle import redirect, abort, response, static_file, request

from .. import app

from ...models import (Session, Mailing, NoResultFound, Item, Category,
                      Recipient, Group, Image, Template, ExternalLink, Article)
from ...html import HTMLPageComposer
from .validators import (validate, ModelListValidator, MailingValidator,
                         CategoryValidator, ItemValidator, InvalidForm,
                         RecipientValidator, GroupValidator)



@app.route('/', template='index.html')
def index():
    return {}

# Generic views

_ = lambda s: s


class ErrorResponse(StandardError):
    pass
 
def generic_collection_view(model, plural, filter=None):
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

def generic_item_view(model, plural):
    def view(id):
        item = model.query.get(id.split('::'))
        return {
            'success': True,
            'total': 1,
             plural: [item.__json__()]
        }
    view.func_name = 'show_'+plural
    return view

def generic_creator(model, validator):
    def func(data):
        form = validate(validator, data)
        ob = model()
        _update_from_form(ob, form)
        return ob
    return func

def generic_new_item(creator, plural):
    def view():
        try:
            data = json.load(request.body)
        except ValueError:
            return _error_response('Invalid JSON data')
        try:
            if isinstance(data, dict):
                items = [creator(data)]
            else:
                items = [creator(d) for d in data]
        except InvalidForm, e:
           return _invalid_form_response(e.form) 
        except ErrorResponse, e:
            return _error_response(str(e))
        for ob in items:
            Session.add(ob)
        Session.commit()
        items = [ob.__json__() for ob in items]
        return {
            'success': True,
            plural: items
        }
    view.func_name = 'new_'+plural
    return view

def generic_updater(validator):
    def func(ob, data):
        form = validate(validator, data)
        _update_from_form(ob, form)
        return ob
    return func

def generic_item_update(model, updater, plural):
    def view(id):
        try:
            data = json.load(request.body)
        except ValueError:
            return _error_response('Invalid JSON data')
        try:
            if isinstance(data, dict):
                ob = model.query.get(id)
                items = [updater(ob, data)]
            else:
                ids = [d['id'] for d in data]
                obs = dict((o.id, o)
                           for o in model.query.filter(model.id.in_(ids)).all())
                items = [updater(obs[d['id']], d) for d in data]
        except InvalidForm, e:
           return _invalid_form_response(e.form) 
        items = [ob.__json__() for ob in items]
        Session.commit()
        return {
            'success': True,
            plural: items
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


app.route('/mailing/')(generic_collection_view(Mailing, 'mailings'))
app.route('/mailing/<id>')(generic_item_view(Mailing, 'mailings'))
app.route('/mailing/<id>', method='DELETE')(generic_item_delete(Mailing))

def _create_mailing(data):
    form = validate(MailingValidator, data)
    ob = Mailing()
    _update_from_form(ob, form)
    if 'xhtml' not in ob.templates:
        tpl = Template.latest_by_type('xhtml')
        if tpl is not None:
            ob.templates['xhtml'] = tpl
        else:
            raise ErrorResponse(
                _('Could not assign a default xhtml template. Please create one first'))
    ob.number = ob.next_number()
    return ob

app.route('/mailing/', method='POST')(
    generic_new_item(_create_mailing, 'mailings'))

app.route('/mailing/<id>', method='PUT')(
    generic_item_update(Mailing, generic_updater(MailingValidator), 'mailings'))


# Item views
app.route('/item/')(generic_collection_view(Item, 'items'))
app.route('/item/<id>')(generic_item_view(Item, 'items'))
app.route('/item/<id>', method='DELETE')(generic_item_delete(Item))

def _create_item(data):
    form = validate(ItemValidator, data)
    type = form.pop('type')
    cls = globals()[type]
    ob = cls()
    _update_from_form(ob, form)
    return ob
app.route('/item/', method='POST')(generic_new_item(_create_item, 'items'))

def _update_item(ob, data):
    form = validate(ItemValidator, data)
    type = form.pop('type')
    cls = globals()[type]
    if ob.type != type:
        Session.delete(ob)
        Session.flush()
        ob = cls(id=ob.id)
        Session.add(ob)
    _update_from_form(ob, form)
    return ob
app.route('/item/<id>', method='PUT')(
    generic_item_update(Item, _update_item, 'items'))


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

app.route('/recipient/')(generic_collection_view(Recipient, 'recipients'))
app.route('/recipient/', method='POST')(
    generic_new_item(
        generic_creator(Recipient, RecipientValidator),
        'recipients'))
app.route('/recipient/<id>')(generic_item_view(Recipient, 'recipients'))
app.route('/recipient/<id>', method='PUT')(
    generic_item_update(Recipient,
                        generic_updater(RecipientValidator), 'recipients'))
app.route('/recipient/<id>', method='DELETE')(generic_item_delete(Recipient))

# Group views

app.route('/group/')(generic_collection_view(Group, 'groups'))
app.route('/group/', method='POST')(
    generic_new_item(
        generic_creator(Group, GroupValidator),
        'groups'))
app.route('/group/<id>')(generic_item_view(Group, 'groups'))
app.route('/group/<id>', method='PUT')(
    generic_item_update(Group,
                        generic_updater(GroupValidator), 'groups'))
app.route('/group/<id>', method='DELETE')(generic_item_delete(Group))

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
