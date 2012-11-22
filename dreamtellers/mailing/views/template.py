from lxml import etree
from pkg_resources import resource_filename

from ..models import Template
from ..dtds import DTDResolver
from .. import app
from ..validators import (Schema, UnicodeString, OneOf, Invalid,
                          format_compound_error)
from .base import rest_views

class TemplateValidator(Schema):
    title = UnicodeString(allow_empty=False)
    type = OneOf(["xhtml", "text"], allow_empty=False)
    body = UnicodeString(allow_empty=False, if_empty=None)

    messages = {
        'invalidXML': 'Invalid XML: %(error)s'
    }

    default_bodies = dict(
        (k, open(resource_filename(__name__, 'default_templates/index.'+k)).read().decode('utf8'))
        for k in ('xhtml', 'text')
    )



    def __init__(self, *args, **kw):
        super(TemplateValidator, self).__init__(*args, **kw)
        self._parser = etree.XMLParser(load_dtd=True)
        self._parser.resolvers.add(DTDResolver())

    def _to_python(self, value, state=None):
        value = super(TemplateValidator, self)._to_python(value, state)
        if not value['body'] or value['body'] in self.default_bodies.values():
            value['body'] = self.default_bodies[value['type']]
        if value['type']=='xhtml':
            try:
                dom = etree.fromstring(value['body'], parser=self._parser)
            except etree.XMLSyntaxError, e:
                error_dict = {
                    'body': Invalid(self.message('invalidXML', state,
                                    error=str(e)), value, state)
                }
                raise Invalid(format_compound_error(error_dict),
                              value, state, error_dict=error_dict)
        return value
                
    
rest_views(app, Template, '/template/', 'templates',
    validator=TemplateValidator
    )
