try:
    import json
except ImportError:
    import simplejson as json

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
    Bool,
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
    'JsonValidator',
    'ISO8601DateValidator',
    'FieldStorageUploadConverter',
    'Bool',
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
    



class Schema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True




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
