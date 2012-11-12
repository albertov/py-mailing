from ...models import SentMailing, GroupSentMailing
from .. import app
from ..validators import Schema, Int, ISO8601DateValidator
from .base import rest_views, generic_creator

class SentMailingValidator(Schema):
    programmed_date = ISO8601DateValidator(allow_empty=False)
    mailing_id = Int(allow_empty=False)

class GroupSentMailingValidator(Schema):
    group_id = Int(allow_empty=False)
    sent_mailing_id = Int(allow_empty=False)

_create_sent_mailing = generic_creator(SentMailing, SentMailingValidator)
def create_sent_mailing(data):
    ob = _create_sent_mailing(data)
    if not ob.groups:
        last_one = SentMailing.least_recently_created()
        if last_one is not None:
            for g in last_one.groups:
                ob.groups.append(g)
    return ob


rest_views(app, SentMailing, '/sent_mailing/', 'sent_mailings',
           validator=SentMailingValidator, creator=create_sent_mailing)
rest_views(app, GroupSentMailing, '/group_sent_mailing/', 'group_sent_mailings',
           validator=GroupSentMailingValidator)
