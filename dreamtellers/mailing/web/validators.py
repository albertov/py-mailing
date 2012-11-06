import json
from formencode import api, schema, validators
from sqlalchemy import sql
from iso8601 import parse_date, ParseError

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
        if hasattr(params, 'read'):
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
        except api.Invalid, e:
            self.errors = e.unpack_errors()
            self.message = unicode(e)

    def __getitem__(self, name):
        return self.params[name]

    def pop(self, *args):
        return self.params.pop(*args)
        

    def __iter__(self):
        return iter(self.params)


class JsonValidator(api.FancyValidator):
    def _to_python(self, value, state=None):
        if value:
            try:
                return json.loads(value)
            except ValueError, e:
                raise api.Invalid(str(e))

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


class ModelListValidator(schema.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    if_key_missing = None

    def __init__(self, model):
        self.model = model
        fields = dict(self.fields,
            sort=SortValidator(model),
            filter=FilterValidator(model),
            )
        super(ModelListValidator, self).__init__(fields=fields)

    id = validators.String(if_missing=None)
    limit = validators.Int(min=0, max=100, if_missing=25)
    page = validators.Int(min=1, if_missing=1)
    start = validators.Int(min=0, if_missing=0)

class ISO8601DateValidator(validators.FancyValidator):
    messages = {
        'invalid': 'Invalid format'
    }
    if_empty=None
    def _to_python(self, value, state=None):
        if value:
            try:
                value = parse_date(value).replace(tzinfo=None)
            except (ParseError, TypeError):
                raise api.Invalid(self.message('invalid', state), value, state)
        return value

class MailingValidator(schema.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ignore_key_missing = True

    date = ISO8601DateValidator(allow_empty=False)
    number = validators.Int(min=0)

class ItemValidator(schema.Schema):
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
    >>> ItemValidator.to_python(dict(base, type='Foo', title='foo'))
    Traceback (most recent call last):
    ...
    Invalid: type: Value must be one of: Article; ExternalLink (not 'Foo')
    """
    allow_extra_fields = True
    filter_extra_fields = True

    category_id = validators.Int(min=0, allow_empty=True, if_missing=None)
    mailing_id = validators.Int(min=0, allow_empty=False)
    title = validators.UnicodeString(allow_empty=False)
    content = validators.UnicodeString(allow_empty=True, if_missing=None)
    type = validators.OneOf(['Article', 'ExternalLink'])
    position = validators.Int(min=0, if_missing=0)
    url = validators.URL(if_missing=None, check_exists=True)

    def _to_python(self, value, state=None):
        value = super(ItemValidator, self)._to_python(value, state)
        if value['type']=='ExternalLink' and not value['url']:
            error_dict = {
                'url': api.Invalid(self.fields['url'].message('empty', state),
                                   value, state)
            }
            raise api.Invalid(schema.format_compound_error(error_dict),
                              value, state, error_dict=error_dict)
        if value['type']=='Article' and not value['content']:
            error_dict = {
                'content': api.Invalid(self.fields['content'].message('empty', state),
                                    value, state)
            }
            raise api.Invalid(schema.format_compound_error(error_dict),
                              value, state, error_dict=error_dict)
        return value

class CategoryValidator(schema.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ignore_key_missing = True

    category_id = validators.Int(min=0)
    title = validators.UnicodeString(allow_empty=False)

class RecipientValidator(schema.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ignore_key_missing = True

    name = validators.UnicodeString(allow_empty=False)
    email = validators.Email(allow_empty=False)
    group_id = validators.Int(min=0)
