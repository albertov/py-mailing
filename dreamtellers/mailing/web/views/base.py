import json

from bottle import redirect, abort, response, static_file, request
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ...models import Session
from ..validators import validate, ModelListValidator, InvalidForm

__all__ = [
    'ErrorResponse',
    'generic_collection_view',
    'generic_show_item',
    'generic_create_item',
    'generic_creator',
    'generic_update_item',
    'generic_updater',
    'generic_delete_item',
    'update_from_form',
    'error_response',
    'invalid_form_response',
    'redirect',
    'abort',
    'response',
    'static_file',
    'request',
    '_',
]

_ = lambda s: s


class ErrorResponse(StandardError):
    pass
 
def generic_collection_view(model, plural, filter=None):
    def view():
        form = validate(ModelListValidator(model), request.params)
        if not form.is_valid:
            return invalid_form_response(form)
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

def generic_show_item(model, plural):
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
        update_from_form(ob, form)
        return ob
    return func

def generic_create_item(creator, plural):
    def view():
        try:
            data = json.load(request.body)
        except ValueError:
            return error_response('Invalid JSON data')
        try:
            if isinstance(data, dict):
                items = [creator(data)]
            else:
                items = [creator(d) for d in data]
        except InvalidForm, e:
           return invalid_form_response(e.form) 
        except ErrorResponse, e:
            return error_response(str(e))
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
        update_from_form(ob, form)
        return ob
    return func

def generic_update_item(model, updater, plural):
    def view(id):
        try:
            data = json.load(request.body)
        except ValueError:
            return error_response('Invalid JSON data')
        try:
            if isinstance(data, dict):
                ob = model.query.get(id.split('::'))
                items = [updater(ob, data)]
            else:
                #FIXME: Implement support for composite pks
                ids = [d['id'] for d in data]
                obs = dict((o.id, o)
                           for o in model.query.filter(model.id.in_(ids)).all())
                items = [updater(obs[d['id']], d) for d in data]
        except InvalidForm, e:
           return invalid_form_response(e.form) 
        items = [ob.__json__() for ob in items]
        Session.commit()
        return {
            'success': True,
            plural: items
        }
    return view

def generic_delete_item(model):
    def delete(id):
        item = model.query.get(id.split('::'))
        if item is not None:
            Session.delete(item)
            Session.commit()
        return {
            'success': True,
        }
    return delete

def rest_views(app, model, url, plural, validator=None, creator=None,
               updater=None, collection_query=None):
                
    item_url = url + '<id>'
    app.route(url)(
        generic_collection_view(model, plural, collection_query)
        )
    app.route(item_url)(generic_show_item(model, plural))
    app.route(item_url, method='DELETE')(generic_delete_item(model))
    if creator is None:
        creator = generic_creator(model, validator)
    app.route(url, method='POST')(generic_create_item(creator, plural))
    if updater is None:
        updater = generic_updater(validator)
    app.route(item_url, method='PUT')(
        generic_update_item(model, updater, plural))

# Utilities

def invalid_form_response(form):
    return error_response(form.message, form.errors)

def error_response(message, errors=None):
    response.status = '400 Bad Request'
    return {
        'success':False,
        'message': message,
        'errors': errors,
    }




def update_from_form(ob, form):
    cls = ob.__class__
    for key in form:
        new_value = form[key]
        desc = getattr(cls, key, None)
        if isinstance(desc, InstrumentedAttribute):
            old_value = getattr(ob, key, None)
            if old_value != new_value:
                setattr(ob, key, new_value)
