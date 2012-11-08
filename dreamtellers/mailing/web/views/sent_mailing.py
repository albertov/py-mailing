from ...models import SentMailing, GroupSentMailing
from .. import app
from ..validators import Schema, Int, ISO8601DateValidator
from .base import rest_views

class SentMailingValidator(Schema):
    programmed_date = ISO8601DateValidator(allow_empty=False)
    mailing_id = Int(allow_empty=False)

class GroupSentMailingValidator(Schema):
    group_id = Int(allow_empty=False)
    sent_mailing_id = Int(allow_empty=False)


rest_views(app, SentMailing, '/sent_mailing/', 'sent_mailings',
           validator=SentMailingValidator)
rest_views(app, GroupSentMailing, '/group_sent_mailing/', 'group_sent_mailings',
           validator=GroupSentMailingValidator)
