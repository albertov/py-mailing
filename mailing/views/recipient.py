from ..models import Recipient
from .. import app
from ..validators import Schema, UnicodeString, Email, Int, Bool
from .base import rest_views

class RecipientValidator(Schema):
    name = UnicodeString(allow_empty=False)
    email = Email(allow_empty=False)
    active = Bool(allow_empty=True)
    group_id = Int(min=0)

rest_views(app, Recipient, '/recipient/', 'recipients',
           validator=RecipientValidator)
