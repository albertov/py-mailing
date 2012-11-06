from ...models import Session, Item

from .. import app
from ..validators import (
    validate,
    Schema,
    Int,
    UnicodeString,
    OneOf,
    URL,
    Invalid,
    format_compound_error
    )
from .base import rest_views, update_from_form

class ItemValidator(Schema):
    """
    >>> base = dict(mailing_id=0, category_id=None)
    >>> v = ItemValidator.to_python(dict(base, type='Article', title='foo', content='foo'))
    >>> ItemValidator.to_python(dict(base, type='Article', title='foo'))
    Traceback (most recent call last):
    ...
    Invalid: content: Please enter a value
    >>> ItemValidator.to_python(dict(base, type='ExternalLink', title='foo'))
    Traceback (most recent call last):
    ...
    Invalid: url: Please enter a value
    >>> ItemValidator.to_python(dict(base, type='Foo', title='foo')) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    Invalid: type: Value must be one of: ... (not 'Foo')
    """
    category_id = Int(min=0, allow_empty=True, if_missing=None)
    mailing_id = Int(min=0, allow_empty=False)
    title = UnicodeString(allow_empty=False)
    content = UnicodeString(allow_empty=True, if_missing=None)
    type = OneOf(Item.available_types())
    position = Int(min=0, if_missing=0)
    url = URL(if_missing=None, check_exists=True)

    def _to_python(self, value, state=None):
        value = super(ItemValidator, self)._to_python(value, state)
        if value['type']=='ExternalLink' and not value['url']:
            error_dict = {
                'url': Invalid(self.fields['url'].message('empty', state),
                                   value, state)
            }
            raise Invalid(format_compound_error(error_dict),
                              value, state, error_dict=error_dict)
        if value['type']=='Article' and not value['content']:
            error_dict = {
                'content': Invalid(self.fields['content'].message('empty', state),
                                    value, state)
            }
            raise Invalid(format_compound_error(error_dict),
                              value, state, error_dict=error_dict)
        return value

def _create(data):
    form = validate(ItemValidator, data)
    type = form.pop('type')
    ob = Item.create_subclass(type)
    update_from_form(ob, form)
    return ob

def _update(ob, data):
    form = validate(ItemValidator, data)
    type = form.pop('type')
    if ob.type != type:
        Session.delete(ob)
        Session.flush()
        ob = Item.create_subclass(type, id=ob.id)
        Session.add(ob)
    update_from_form(ob, form)
    return ob

rest_views(app, Item, '/item/', 'items', creator=_create, updater=_update)