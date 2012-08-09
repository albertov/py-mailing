import json
from formencode import api, schema, validators
from sqlalchemy import sql

class validate(object):
    def __init__(self, validator, params):
        self.params = dict(params)
        self.errors = None
        self.message = ''
        self.validator = validator
        self._validate()

    @property
    def is_valid(self):
        return not self.errors

    def _validate(self):
        try:
            self.params = self.validator.to_python(self.params)
        except api.Invalid, e:
            self.errors = e.unpack_errors()
            self.message = unicode(e)

    def __getitem__(self, name):
        return self.params[name]

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


class ModelListValidator(schema.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    if_key_missing = None

    def __init__(self, model):
        self.model = model
        fields = dict(self.fields, sort=SortValidator(model))
        super(ModelListValidator, self).__init__(fields=fields)

    limit = validators.Int(min=0, max=100, if_missing=25)
    page = validators.Int(min=1, if_missing=1)
    start = validators.Int(min=0, if_missing=0)
