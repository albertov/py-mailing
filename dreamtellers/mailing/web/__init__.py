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

@app.route('/m/<number:int>/')
def mailing(number, db):
    return _get_composer(db, number).get_file('index.html').data

@app.route('/m/<number:int>/<filename:re:.+>')
def mailing_file(number, filename, db):
    f = _get_composer(db, number).get_file(filename)
    response.content_type = f.content_type
    return f.data

@app.route('/mailing/<id>/item_tree/')
def mailing_item_tree(id, db):
    mailing = db.query(Mailing).get(id)
    category_items = {}
    roots = []
    for category, items in mailing.grouped_items:
        root = category.path.next()
        if root not in roots:
            roots.append(root)
        assert category not in category_items
        category_items[category] = list(items)
    def make_category_node(category):
        items = category_items.get(category, [])
        children = [dict(i.__json__(), leaf=True, id='item-%d'%i.id)
                    for i in items]
        children.extend(make_category_node(c) for c in category.subcategories)
        return dict(category.__json__(),
                    id='category-%d'%category.id,
                    expanded=True,
                    children=children)
    return {'success': True, 'children': map(make_category_node, roots)}
    

 
def collection_view(model, plural=None):
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
    def show(id, db):
        item = db.query(model).get(id.split('::'))
        return {
            'success': True,
            'total': 1,
             plural: [item.__json__()]
        }
    def delete(id, db):
        item = db.query(model).get(id.split('::'))
        db.delete(item)
        return {
            'success': True,
        }
    def view(id, db):
        if request.method=='GET':
            return show(id, db)
        elif request.method=='DELETE':
            return delete(id, db)
        else:
            response.status = '405 Method Not Allowed'
            return {}
    view.func_name = 'show_'+plural
    return view

app.route('/mailing/')(collection_view(Mailing))
app.route('/mailing/<id>')(item_view(Mailing))

app.route('/item/')(collection_view(Item))
app.route('/image/')(collection_view(Image))
app.route('/recipient/')(collection_view(Recipient))
app.route('/group/')(collection_view(Group))

app.route('/category/')(collection_view(Category, 'categories'))
app.route('/category/<id>')(item_view(Category, 'categories'))


def _get_composer(db, number):
    try:
        m = db.query(Mailing).filter_by(number=number).one()
    except NoResultFound:
        abort(404)
    return HTMLPageComposer(m)

@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=resource_filename(__name__, 'static'))
