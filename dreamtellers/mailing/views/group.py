from ..models import Group
from .. import app
from ..validators import Schema, UnicodeString, Int
from .base import rest_views

class GroupValidator(Schema):
    name = UnicodeString(allow_empty=False)
    description = UnicodeString(allow_empty=True)
    priority = Int(min=0)

rest_views(app, Group, '/group/', 'groups', validator=GroupValidator)
