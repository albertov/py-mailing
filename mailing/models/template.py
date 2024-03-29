import re
import sys
import traceback
import datetime

from lxml import etree

from sqlalchemy import (Column, ForeignKey, DateTime, Integer, Unicode, orm,
                        Table, String, sql, Boolean)
from sqlalchemy.ext.hybrid import hybrid_property

from babel.dates import format_date

from markupsafe import escape

from genshi.template import MarkupTemplate, TemplateSyntaxError
from genshi.template.eval import UndefinedError

from mako.template import Template as MakoTemplate
from mako.exceptions import RichTraceback

from . import Model
from .image import Image
from .config import Config

template_image_table = Table("template_image", Model.metadata,
    Column('template_id', Integer, ForeignKey('template.id', ondelete="CASCADE", onupdate="CASCADE"),
           primary_key=True),
    Column('image_id', Integer, ForeignKey('image.id', ondelete="CASCADE", onupdate="CASCADE"),
           primary_key=True)
)


class Template(Model):
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False, unique=True)
    type = Column(String(20), nullable=False, default='xhtml')
    _body = Column('body', Unicode, nullable=False)

    debug = Column(Boolean, nullable=False, default=True)

    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)

    images = orm.relation(Image, secondary=template_image_table, lazy=True)

    variables =  dict(
        Config = Config,
        format_date = format_date
        )

    __content_types__ = {
        'xhtml': 'text/html',
        'text': 'text/plain',
    }



    @property
    def content_type(self):
        return self.__content_types__[self.type]



    @hybrid_property
    def body(self):
        return self._body

    @body.setter
    def _body_setter(self, value):
        self._body = value
        self.images = self._find_images(value)

    @body.expression
    def _body_expression(cls):
        return cls._body

    @property
    def body_lines(self):
        return self.body.splitlines()
    
    def _find_images(self, body):
        dom = etree.HTML(body)
        filenames = []
        for e in dom.xpath('//*[@background]'):
            filenames.append(e.attrib['background'])
        for e in dom.xpath('//img[@src]'):
            filenames.append(e.attrib['src'])
        return filter(None, map(Image.by_filename, filenames))

    def __repr__(self):
        data = (self.id, self.title)
        return self.__class__.__name__ + repr(data)

    def render(self, **data):
        if self.type == 'text':
            return self._render_text(**data)
        else:
            return self._render_xhtml(**data)

    def _render_xhtml(self, **data):
        namespace = dict(self.variables, **data)
        def render():
            tpl = MarkupTemplate(self.body)
            stream = tpl.generate(**namespace)
            o = stream.render(self.type)
            return o.decode('utf8') #FIXME: Derive from <meta http-equiv> if present

        if not self.debug:
            return render()

        try:
            return render()
        except TemplateSyntaxError, e:
            return self._render_html_error(e, e.lineno)
        except UndefinedError, e:
            var_name = re.search(r'"(.*?)"', e.message).group(1) 
            r = re.compile(r'\b%s\b'%(var_name,))
            lineno = None
            for i, l in enumerate(self.body_lines):
                if r.search(l):
                    lineno = i+1
                    break
            return self._render_html_error(e, lineno)
        except Exception, e:
            # assume exception ocurred in template
            frame = traceback.extract_tb(sys.exc_info()[2])[-1]
            lineno, function_name = frame[1:-1]
            err = "In %s: %s" % (escape(function_name),
                                 escape(str(e)))
            return self._render_html_error(err, lineno)

    def _render_text(self, **data):
        namespace = dict(self.variables, **data)
        def render():
            tpl = MakoTemplate(self.body,
                default_filters=['decode.utf8'],
                )
            return tpl.render_unicode(**namespace)

        if not self.debug:
            return render()

        try:
            return render()
        except:
            tb = RichTraceback()
            lineno, function = tb.traceback[-1][1:3]
            return self._render_text_error(tb.error, lineno)

    def _render_text_error(self, e, lineno=None, context=2):
        olines = []
        if lineno is not None:
            lines = list(enumerate(self.body_lines))
            lines = lines[max(lineno-1-context,0):lineno+context]
            for i, line in lines:
                olines.append(u'%s%s: %s' % (
                    '-->' if i+1==lineno else '   ',
                    i+1,
                     _ellipsis(line, 150)
                ))
        return u'Error en plantilla "%s"\n%s\n\n%s' % (
                    self.title, e, '\n'.join(olines))
            

    def _render_html_error(self, e, lineno=None, context=2):
        olines = []
        if lineno is not None:
            lines = list(enumerate(self.body_lines))
            lines = lines[max(lineno-1-context,0):lineno+context]
            for i, line in lines:
                color = '#f00' if i+1==lineno else '#888'
                olines.append(
                    u'<span>%s:</span><span style="color:%s">%s</span>' % (
                        i+1,
                        color,
                        escape(_ellipsis(line, 150)),
                     ))
        return (u'<h1>Error en plantilla <em>%s</em></h1>'
                u'<b>%s</b><br />%s' % (
                    self.title, e, '<br />'.join(olines),
                ))

        
    def __json__(self):
        return dict(
            id=self.id,
            title=self.title,
            type=self.type,
            body=self.body,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
            )

def _ellipsis(s, l):
    m = l-3
    return s[:m] + ('...' if len(s)>m else '')
