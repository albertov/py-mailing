from ...models import MailingDelivery, GroupMailingDelivery
from .. import app
from ..validators import Schema, Int, ISO8601DateValidator
from .base import rest_views, generic_creator

class MailingDeliveryValidator(Schema):
    programmed_date = ISO8601DateValidator(allow_empty=False)
    mailing_id = Int(allow_empty=False)

class GroupMailingDeliveryValidator(Schema):
    group_id = Int(allow_empty=False)
    mailing_delivery_id = Int(allow_empty=False)

_create_mailing_delivery = generic_creator(MailingDelivery, MailingDeliveryValidator)
def create_mailing_delivery(data):
    ob = _create_mailing_delivery(data)
    if not ob.groups:
        last_one = MailingDelivery.least_recently_created()
        if last_one is not None:
            for g in last_one.groups:
                ob.groups.append(g)
    return ob


rest_views(app, MailingDelivery, '/mailing_delivery/', 'mailing_deliveries',
           validator=MailingDeliveryValidator, creator=create_mailing_delivery)
rest_views(app, GroupMailingDelivery, '/group_mailing_delivery/',
           'group_mailing_deliveries', validator=GroupMailingDeliveryValidator)
