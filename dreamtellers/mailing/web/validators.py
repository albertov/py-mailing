import json

from sqlalchemy import sql

from formencode.api import Invalid
from formencode.schema import Schema, format_compound_error
from formencode.validators import (
    Int,
    UnicodeString,
    OneOf,
    FancyValidator,
    String,
    URL,
    Email,
    FieldStorageUploadConverter,
)

from .iso8601 import parse_date, ParseError

__all__ = [
    'format_compound_error',
    'validate',
    'InvalidForm',
    'Invalid',

    'Schema',
    'FancyValidator',
    'Int',
    'String',
    'URL',
    'Email',
    'UnicodeString',
    'OneOf',
    'SortValidator',
    'JsonValidator',
    'ModelListValidator',
    'ISO8601DateValidator',
    'FieldStorageUploadConverter',
]

class InvalidForm(StandardError):
    def __init__(self, form):
        self.form = form

    def __unicode__(self):
        return self.form.message

class validate(object):
    def __init__(self, validator, params, raises=True):
        self.errors = None
        self.message = ''
        self.validator = validator
        self.raises = raises
        self.params = self._decode_params(params)
        if self.params is not None:
            self._validate()
        if raises and not self.is_valid:
            raise InvalidForm(self)

    def _decode_params(self, params):
        if hasattr(params.__class__, 'read'):
            try:
                return json.load(params)
            except ValueError:
                self.message = 'Invalid JSON data'
                self.errors = {}
                return None
        else:
            return dict(params)

    @property
    def is_valid(self):
        return self.errors is None

    def _validate(self):
        try:
            self.params = self.validator.to_python(self.params)
        except Invalid, e:
            self.errors = e.unpack_errors()
            self.message = unicode(e)

    def __getitem__(self, name):
        return self.params[name]

    def pop(self, *args):
        return self.params.pop(*args)
        

    def __iter__(self):
        return iter(self.params)


class JsonValidator(FancyValidator):
    def _to_python(self, value, state=None):
        if value:
            try:
                return json.loads(value)
            except ValueError, e:
                raise Invalid(str(e))

    def _from_python(self, value):
        return json.dumps(value)
    

class SortValidator(JsonValidator):
    if_missing = None

    def __init__(self, model):
        self.model = model

    def _to_python(self, value, state=None):
        value = super(SortValidator, self)._to_python(value, state)
        if value:
            ret = []
            for v in value:
                col = getattr(self.model, v['property'])
                if v.get('direction', 'ASC') == 'DESC':
                    col = sql.desc(col)
                ret.append(col)
            return ret


class FilterValidator(JsonValidator):
    if_missing = None

    def __init__(self, model):
        self.model = model

    def _to_python(self, value, state=None):
        value = super(FilterValidator, self)._to_python(value, state)
        if value:
            ret = []
            for v in value:
                col = getattr(self.model, v['property'])
                ret.append(col==v['value'])
            return ret


class Schema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ignore_key_missing = True


class ModelListValidator(Schema):
    if_key_missing = None

    def __init__(self, model):
        self.model = model
        fields = dict(self.fields,
            sort=SortValidator(model),
            filter=FilterValidator(model),
            )
        super(ModelListValidator, self).__init__(fields=fields)

    id = String(if_missing=None)
    limit = Int(min=0, max=100, if_missing=25)
    page = Int(min=1, if_missing=1)
    start = Int(min=0, if_missing=0)


class ISO8601DateValidator(FancyValidator):
    messages = {
        'invalid': 'Invalid format'
    }
    if_empty=None
    def _to_python(self, value, state=None):
        if value:
            try:
                value = parse_date(value).replace(tzinfo=None)
            except (ParseError, TypeError):
                raise Invalid(self.message('invalid', state), value, state)
        return value
