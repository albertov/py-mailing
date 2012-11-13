from ...models import Mailing, Template, Image
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

@app.route('/m/<number:int>/<filename:re:.*>')
def mailing_file(number, filename):
    filename = filename or 'index.html'
    if filename not in ['index.html', 'index.txt']:
        # Try to take shortcut if filename is probably an image
        img = Image.by_filename(filename)
        if img is not None:
            redirect(img.url)
    f = _get_composer(number).get_file(filename)
    if f is None:
        abort(404)
    else:
        response.content_type = f.content_type
        return f.data

def _get_composer(number, eager=True):
    m = Mailing.by_number(number, eager)
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
