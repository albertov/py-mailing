from ...models import Recipient
from .. import app
from ..validators import Schema, UnicodeString, Email, Int
from .base import rest_views

class RecipientValidator(Schema):
    name = UnicodeString(allow_empty=False)
    email = Email(allow_empty=False)
    group_id = Int(min=0, if_missing=None)

rest_views(app, Recipient, '/recipient/', 'recipients',
           validator=RecipientValidator)
