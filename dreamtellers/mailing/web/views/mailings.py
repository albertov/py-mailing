from ...models import Mailing, Template
from ...html import HTMLPageComposer

from .. import app
from ..validators import validate, Schema, Int, ISO8601DateValidator
from .base import (
    _,
    response,
    redirect,
    abort,
    rest_views,
    update_from_form,
    ErrorResponse,
    )

class MailingValidator(Schema):
    date = ISO8601DateValidator(allow_empty=False)
    number = Int(min=0)

@app.route('/m/<number:int>/')
def mailing_by_number(number):
    try:
        return _get_composer(number).get_file('index.html').data
    except LookupError:
        abort(404)

@app.route('/m/<number:int>/<filename:re:.+>')
def mailing_file(number, filename):
    try:
        f = _get_composer(number).get_file(filename)
    except LookupError:
        abort(404)
    if hasattr(f, 'url'):
        redirect(f.url)
    else:
        response.content_type = f.content_type
        return f.data

def _get_composer(number):
    m = Mailing.by_number(number, eager=True)
    if m is not None:
        return HTMLPageComposer(m)
    else:
        abort(404)

def _create_mailing(data):
    form = validate(MailingValidator, data)
    ob = Mailing()
    update_from_form(ob, form)
    if 'xhtml' not in ob.templates:
        tpl = Template.latest_by_type('xhtml')
        if tpl is not None:
            ob.templates['xhtml'] = tpl
        else:
            raise ErrorResponse(
                _('Could not assign a default xhtml template. Please create one first'))
    ob.number = ob.next_number()
    return ob

rest_views(app, Mailing, '/mailing/', 'mailings',
           validator=MailingValidator, creator=_create_mailing)
