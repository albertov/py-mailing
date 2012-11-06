from ...models import Group
from .. import app
from ..validators import Schema, UnicodeString
from .base import rest_views

class GroupValidator(Schema):
    name = UnicodeString(allow_empty=False)
    description = UnicodeString(allow_empty=True, if_missing=None)

rest_views(app, Group, '/group/', 'groups', validator=GroupValidator)
