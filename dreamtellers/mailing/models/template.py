import re
import sys
import traceback
import datetime
import os

from sqlalchemy import (Column, ForeignKey, DateTime, Integer, Unicode, orm,
                        Table, String, sql)

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
    Column('template_id', Integer, ForeignKey('template.id', ondelete="CASCADE"),
           primary_key=True),
    Column('image_id', Integer, ForeignKey('image.id', ondelete="CASCADE"),
           primary_key=True)
)

class Template(Model):
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False, unique=True)
    type = Column(String(20), nullable=False, default='xhtml')
    body = Column(Unicode, nullable=False)

    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)

    images = orm.relation(Image, secondary=template_image_table, lazy=True)

    variables =  dict(
        Config = Config,
        format_date = format_date
        )

    @property
    def body_lines(self):
        return self.body.splitlines()
    

    @classmethod
    def latest_by_type(cls, type):
        q = cls.query.filter_by(type=type)
        q = q.order_by(sql.desc(cls.modified))
        return q.first()


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

        if 'RAISE_TEMPLATE_ERRORS' in os.environ:
            return render()

        try:
            return render()
        except TemplateSyntaxError, e:
            return self._render_html_error(e, e.lineno)
        except UndefinedError, e:
            var_name = re.search(r'"(.*?)"', e.message).group(1) 
            r = re.compile(r'\b{0}\b'.format(var_name))
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
            err = "In {function_name}: {e}".format(
                function_name = escape(function_name),
                e = escape(str(e))
                )
            return self._render_html_error(err, lineno)

    def _render_text(self, **data):
        namespace = dict(self.variables, **data)
        def render():
            tpl = MakoTemplate(self.body,
                default_filters=['decode.utf8'],
                )
            return tpl.render_unicode(**namespace)
        if 'RAISE_TEMPLATE_ERRORS' in os.environ:
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
                olines.append(
                    u'{arrow}{lineno}: {line}'.format(
                        line = _ellipsis(line, 150),
                        lineno = i+1,
                        arrow = '-->' if i+1==lineno else '   '
                ))
        return (u'Error en plantilla "{title}"\n'
                u'{error}\n\n{lines}').format(
                    error=e,
                    lines='\n'.join(olines),
                    title=self.title
                )
            

    def _render_html_error(self, e, lineno=None, context=2):
        olines = []
        if lineno is not None:
            lines = list(enumerate(self.body_lines))
            lines = lines[max(lineno-1-context,0):lineno+context]
            for i, line in lines:
                color = '#f00' if i+1==lineno else '#888'
                olines.append((
                    u'<span>{lineno}:</span>'
                    u'<span style="color:{color}">{line}</span>'
                    ).format(
                        color=color,
                        line=escape(_ellipsis(line, 150)),
                        lineno=i+1
                     ))
        return (u'<h1>Error en plantilla <em>{title}</em></h1>'
                u'<b>{error}</b><br />{lines}').format(
                    error=e,
                    lines='<br />'.join(olines),
                    title=self.title
                )

        
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
