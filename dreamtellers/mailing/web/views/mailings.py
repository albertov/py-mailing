from ...models import Mailing, MailingTemplate, Template, Image
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

@app.route('/m/<number:int>/<filename:re:.*>', name='mailing_file')
def mailing_file(number, filename):
    filename = filename or 'index.html'
    if filename not in ['index.html', 'index.txt']:
        # Try to take shortcut if filename is probably an image
        img = Image.by_filename(filename)
        if img is not None:
            redirect(img.internal_url)
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
    lrc = Mailing.least_recently_created()
    if lrc is not None:
        ob.templates = lrc.templates
    ob.number = ob.next_number()
    return ob

rest_views(app, Mailing, '/mailing/', 'mailings',
           validator=MailingValidator, creator=_create_mailing)

class MailingTemplateValidator(Schema):
    mailing_id = Int(allow_empty=False)
    template_id = Int(allow_empty=False)

rest_views(app, MailingTemplate, '/mailing_template/', 'mailing_templates',
           validator=MailingTemplateValidator)
