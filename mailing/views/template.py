from lxml import etree
from pkg_resources import resource_filename

from ..models import Template, Session
from ..dtds import DTDResolver
from .. import app
from ..validators import (validate, Schema, UnicodeString, OneOf, Invalid,
                          format_compound_error, FieldStorageUploadConverter)
from .base import (rest_views, error_handler, request, json_on_html,
                   error_response, update_from_form, abort, response)


class TemplateXHTMLBodyValidator(UnicodeString):
    messages = {
        'invalidXML': 'Invalid XML: %(error)s'
    }

    _parser = etree.XMLParser(load_dtd=True)
    _parser.resolvers.add(DTDResolver())

    def _to_python(self, value, state=None):
        if value:
            try:
                etree.fromstring(value, parser=self._parser).getroottree()
            except etree.XMLSyntaxError, e:
                raise Invalid(self.message('invalidXML', state,
                              error=str(e)), value, state)
        return super(TemplateXHTMLBodyValidator, self)._to_python(value, state)
    

class TemplateValidator(Schema):
    title = UnicodeString(allow_empty=False)
    type = OneOf(["xhtml", "text"], allow_empty=False)
    body = UnicodeString(allow_empty=False, if_empty=None)

    default_bodies = dict(
        (k, open(resource_filename(__name__, 'default_templates/index.'+k)).read().decode('utf8'))
        for k in ('xhtml', 'text')
    )


    def _to_python(self, value, state=None):
        value = super(TemplateValidator, self)._to_python(value, state)
        if not value['body'] or value['body'] in self.default_bodies.values():
            value['body'] = self.default_bodies[value['type']]
        if value['type']=='xhtml':
            try:
                v = value['body']
                value['body'] = TemplateXHTMLBodyValidator.to_python(v, state)
            except Invalid, e:
                error_dict = {'body': e}
                raise Invalid(format_compound_error(error_dict),
                              value, state, error_dict=error_dict)
        return value
                
    
rest_views(app, Template, '/template/', 'templates',
    validator=TemplateValidator
    )

class TemplateUploadValidator(TemplateValidator):
    body = FieldStorageUploadConverter(allow_empty=False)

    def _to_python(self, value, state=None):
        value = Schema._to_python(self, value, state)
        if value['body'] and hasattr(value['body'], 'file'):
            body = value['body'].file.read()
            try:
                value['body'] = body.decode('utf8')
            except UnicodeDecodeError, e:
                error_dict = {'body': str(e)}
                raise Invalid(format_compound_error(error_dict),
                              value, state, error_dict=error_dict)
        return super(TemplateUploadValidator, self)._to_python(value, state)


@app.post('/template/<id>', name='template.upload')
@error_handler
def upload_body(id):
    ob = Template.query.get(id)
    if ob is None:
        abort(404)
    form = validate(TemplateUploadValidator(ignore_key_missing=True),
                    request.POST, raises=False)
    if not form.is_valid:
        resp = error_response(form.message, form.errors)
    else:
        update_from_form(ob, form)
        Session.commit()
        resp = dict(
            success=True,
            templates=[ob.__json__()],
        )
    return json_on_html(resp)

@app.get('/template/<id>/body', name='template.body')
def raw_body(id):
    ob = Template.query.get(id)
    if ob is None:
        abort(404)
    response.content_type = '%s; charset=UTF8'%ob.content_type
    response.headers['Content-Disposition'] =\
        'attachment;filename='+ob.title.encode('utf8')
    return ob.body.encode('utf8')
