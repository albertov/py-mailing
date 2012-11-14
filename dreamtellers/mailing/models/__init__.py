#coding: utf8
from itertools import groupby, chain
from operator import attrgetter
from cStringIO import StringIO
from hashlib import md5
import textwrap
import datetime
import re
import traceback
import sys
import os

from babel.dates import format_date

from lxml import etree, builder

import markdown
from markupsafe import escape

from sqlalchemy import (Column, ForeignKey, DateTime, Integer, Unicode, orm,
                        Table, LargeBinary, String, MetaData, sql, event,
                        create_engine)
from sqlalchemy.orm import deferred, joinedload_all
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.hybrid import hybrid_property

from ..util import sniff_content_type

metadata = MetaData()
Model = declarative_base(metadata=metadata)
Session = orm.scoped_session(
    orm.sessionmaker(autoflush=False, autocommit=False)
    )
Model.query = Session.query_property()


from .config import Config

class FileLookupError(LookupError):
    pass

class MissingTemplate(FileLookupError):
    pass



@event.listens_for(orm.mapper, 'before_update')
def update_modified_time(mapper, connection, instance):
    if hasattr(mapper.c, 'modified'):
        instance.modified = datetime.datetime.now()


class Image(Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    hash = Column(String(32), unique=True, nullable=False)
    filename = Column(Unicode(255), nullable=False, unique=True)
    title = Column(Unicode(512))
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    _data = deferred(Column('data', LargeBinary(), nullable=False))
    content_type = Column(String(20), nullable=False)

    @classmethod
    def by_hash(cls, hash, undefer_data=True):
        try:
            q = cls.query.filter_by(hash=hash)
            if undefer_data:
                q = q.options(orm.undefer('data'))
            return q.one()
        except NoResultFound:
            return None

    @classmethod
    def by_filename(cls, filename):
        try:
            return cls.query.filter_by(filename=filename).one()
        except NoResultFound:
            return None

    @hybrid_property
    def data(self):
        return self._data

    @data.setter
    def data_setter(self, value):
        self.content_type = sniff_content_type(value)
        self.hash = md5(value).hexdigest()
        self._data = value

    @data.expression
    def data_expr(cls):
        return cls._data

    @property
    def url(self):
        from .web import app
        return app.get_url('image_view', hash=self.hash)

    PIL_MAP = {
        'image/jpeg': 'JPEG',
        'image/gif': 'GIF',
        'image/png': 'PNG',
    }
    def thumbnail(self, width, height):
        import Image
        img = Image.open(StringIO(self.data))
        img.thumbnail((width, height), Image.ANTIALIAS)
        return self._dump_image(img, self.content_type)

    @classmethod
    def _dump_image(cls, img, content_type):
        buf = StringIO()
        try:
            format = cls.PIL_MAP[content_type]
        except IndexError:
            return None
        img.save(buf, format)
        return buf.getvalue()
        
    @classmethod
    def blank_image(cls, width, height, content_type='image/png'):
        import Image
        img = Image.new('RGBA', (width, height))
        return cls._dump_image(img, content_type)
        

    def __repr__(self):
        data = (self.id, self.title, self.filename)
        return self.__class__.__name__ + repr(data)

    def __json__(self):
        return dict(
            id=self.id,
            title=self.title,
            filename=self.filename,
            content_type=self.content_type,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
            url=self.url,
            )

class Category(Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    image_id = Column(Integer, ForeignKey("image.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

    image = orm.relation(Image, lazy='joined')
    subcategories = orm.relation("Category",
        backref = orm.backref('category', remote_side=[id]),
        lazy='joined',
        join_depth=3)
                            
    @classmethod
    def roots(cls):
        return cls.query.filter_by(category_id=None)

    @property
    def path(self):
        if self.category:
            for p in self.category.path:
                yield p
        yield self

    def __repr__(self):
        data = (self.id, self.title, self.image)
        return self.__class__.__name__ + repr(data)

    def __json__(self):
        return dict(
            id=self.id,
            title=self.title,
            image_id=self.image_id,
            image=self.image.__json__() if self.image is not None else None,
            categories = [c.__json__() for c in self.subcategories],
            category_id=self.category_id,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
            )

class Item(Model):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    type = Column(String(20), nullable=False)
    position = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey('category.id'))
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    mailing_id = Column(Integer, ForeignKey('mailing.id', ondelete='CASCADE',
                                            onupdate='CASCADE'),
                       nullable=False)
    image_id = Column(Integer, ForeignKey("image.id"))

    image = orm.relation(Image, lazy='joined')
    image_position = Column(String(1), nullable=False, default="l")


    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'Item',
                       'with_polymorphic': '*'}

    category = orm.relation( Category,
        backref=orm.backref('items'),
        lazy=True)

    @classmethod
    def create_subclass(cls, type, **kw):
        subcls = orm.class_mapper(cls).polymorphic_map[type].class_
        return subcls(**kw)

    @classmethod
    def available_types(cls):
        return list(orm.class_mapper(cls).polymorphic_map)

    def __repr__(self):
        data = (self.id, self.title, self.category.title)
        return self.__class__.__name__ + repr(data)

    def __json__(self):
        return dict(
            id=self.id,
            title=self.title,
            position=self.position,
            type=self.type,
            category_id=self.category_id,
            mailing_id=self.mailing_id,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
            image_id = self.image_id,
            image_position = self.image_position,
            image=self.image.__json__() if self.image is not None else None,
            content = self.content,
            )

@event.listens_for(Item, 'before_update', propagate=True)
@event.listens_for(Item, 'before_delete', propagate=True)
@event.listens_for(Item, 'before_insert', propagate=True)
def update_mailing_modified_time(mapper, connection, instance):
    stmt = Mailing.__table__.update().where(Mailing.id==instance.mailing_id)
    stmt = stmt.values(modified=datetime.datetime.now())
    connection.execute(stmt)

class ExternalLink(Item):
    __tablename__ = "external_link"
    id = Column(Integer, ForeignKey("item.id"), primary_key=True)
    content = Column(Unicode)
    url = Column(Unicode, nullable=False)
    __mapper_args__ = {'polymorphic_identity':'ExternalLink'}

    def __json__(self):
        return dict(super(ExternalLink, self).__json__(),
            content = self.content or None,
            url = self.url,
            )

class Article(Item):
    __tablename__ = 'article'
    __mapper_args__ = {'polymorphic_identity':'Article'}

    id = Column(Integer, ForeignKey("item.id"), primary_key=True)
    content = Column(Unicode, nullable=False)

    @property
    def url(self):
        return "#art-%d"%self.position

    @property
    def anchor(self):
        return "art-%d"%self.position


    @property
    def html(self):
        dom = etree.HTML('<div>%s</div>' % markdown.markdown(self.content))
        self._insert_image(dom)
        return '\n'.join(etree.tounicode(e, method='xml')
                         for e in dom.getchildren())

    def plain_text(self, width=79):
        dom = etree.HTML('<div>%s</div>' % markdown.markdown(self.content))
        for e in dom.xpath('//a'):
            if 'href' in e.attrib:
                e.tag = 'span'
                e.text += u' ({0})'.format(e.attrib.pop('href'))
        text = '\n\n'.join(etree.tounicode(e, method='text')
                         for e in dom.getchildren())
        return textwrap.fill(text, width)

    def _insert_image(self, dom):
        if self.image:
            ps = dom.xpath('//p[1]')
            if ps:
                p = ps[0]
                img = builder.E.img(src=self.image.filename)
                if self.image.title:
                    img.attrib['title'] = img.attrib['alt'] = self.image.title
                class_ = 'left' if self.image_position=='l' else 'right'
                img.attrib["class"] = class_
                p.insert(0, img)
                img.tail = p.text
                p.text = None

    def __json__(self):
        return dict(super(Article, self).__json__(),
            content = self.content,
            )

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
        from genshi.template import MarkupTemplate, TemplateSyntaxError
        from genshi.template.eval import UndefinedError
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
        from mako.template import Template
        from mako.exceptions import RichTraceback
        module_directory = '/tmp/mako_templates' #FIXME
        def render():
            tpl = Template(self.body,
                module_directory=module_directory,
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

class Group(Model):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    description = Column(Unicode)
    priority = Column(Integer, nullable=False, default=0)
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)


    __mapper_args__ = {'order_by':priority}

    def __repr__(self):
        data = (self.id, self.name)
        return self.__class__.__name__ + repr(data)

    def __json__(self):
        return dict(
            id=self.id,
            name=self.name,
            priority=self.priority,
            description=self.description or None,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
            )

class Recipient(Model):
    __tablename__ = "recipient"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"))
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)

    group = orm.relation(Group,  backref='recipients')
    
    def __repr__(self):
        data = (self.id, self.name, self.email)
        return self.__class__.__name__ + repr(data)


    def __json__(self):
        return dict(
            id=self.id,
            name=self.name,
            email=self.email,
            group_id=self.group_id,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
            )



mailing_template_table = Table("mailing_template", Model.metadata,
   Column('mailing_id', ForeignKey('mailing.id', ondelete='CASCADE'),
          primary_key=True),
    Column('template_id', ForeignKey('template.id', ondelete='CASCADE'),
           primary_key=True)
)
                            

class Mailing(Model):
    __tablename__ = "mailing"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True, nullable=False, default=0)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)

    items = orm.relation(Item, collection_class=ordering_list('position'),
                         order_by=Item.position, backref='mailing',
                         lazy=True, cascade='all,delete-orphan')
    templates = orm.relation(Template, secondary=mailing_template_table,
                             collection_class=attribute_mapped_collection('type'),
                             lazy=True)


    @classmethod
    def by_number(cls, number, eager=True):
        q = cls.query.filter_by(number=number)
        if eager:
            q = q.options(
                joinedload_all('items.image'),
                joinedload_all('templates.images'),
                joinedload_all('items.category.image'),
                joinedload_all('items.category.subcategories'),
            )
        try:
            return q.one()
        except NoResultFound:
            return None

    @classmethod
    def next_number(cls):
        query = sql.select([sql.func.max(cls.number)])
        return (Session.execute(query).scalar() or 0) + 1

    @property
    def grouped_items(self):
        return groupby(self.items, attrgetter('category'))

    @property
    def url(self):
        #FIXME
        return "http://dreamtellers.org/boletines/{0:03}/".format(self.number)


    @property
    def images(self):
        images = set()
        for t in self.templates.values():
            images.update(t.images)
        for i in self.items:
            if i.category and i.category.image:
                images.add(i.category.image)
            if hasattr(i, 'image') and i.image is not None:
                images.add(i.image)
        return list(images)

    def get_file(self, filename):
        try:
            return [i for i in self.images if i.filename==filename][0]
        except IndexError:
            raise FileLookupError(filename)

    def items_by_type(self, type, grouped=False):
        items =  [i for i in self.items if i.type==type]
        if grouped:
            items = groupby(items, attrgetter('category'))
        return items

    def render(self, format='xhtml', **kw):
        ns = dict(kw, mailing=self)
        try:
            tpl = self.templates[format]
        except KeyError:
            raise MissingTemplate(format)
        else:
            return tpl.render(**ns)

    def __repr__(self):
        data = (self.number, self.date, len(self.items))
        return self.__class__.__name__ + repr(data)

    def __json__(self):
        return dict(
            id=self.id,
            number=self.number,
            date=self.date.isoformat() if self.date else None,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
        )
        
class GroupSentMailing(Model):
    __tablename__ = 'group_sent_mailing'
    group_id = Column(Integer, ForeignKey('group.id', ondelete="CASCADE"),
                      primary_key=True, nullable=False)
    sent_mailing_id = Column(Integer,
                             ForeignKey('sent_mailing.id', ondelete="CASCADE"),
                             primary_key=True, nullable=False)

    def __json__(self):
        return dict(
            id='::'.join(map(str, [self.group_id, self.sent_mailing_id])),
            group_id=self.group_id,
            sent_mailing_id=self.sent_mailing_id,
        )

class SentMailingProcessedRecipient(Model):
    __table__ = Table('sent_mailing_processed_recipient', metadata,
        Column("recipient_id", Integer,
               ForeignKey('recipient.id', ondelete="CASCADE"),
               primary_key=True, nullable=False),
        Column("sent_mailing_id", Integer,
               ForeignKey('sent_mailing.id', ondelete="CASCADE"),
               primary_key=True, nullable=False),
        Column("time", DateTime, nullable=False,
               default=datetime.datetime.now),
   )

    def __json__(self):
        return dict(
            id='::'.join(map(str, [self.recipient_id, self.sent_mailing_id])),
            recipient_id=self.recipient_id,
            sent_mailing_id=self.sent_mailing_id,
        )

class SentMailing(Model):
    __table__ = Table('sent_mailing', metadata,
        Column("id", Integer, primary_key=True),
        Column("mailing_id", Integer, ForeignKey('mailing.id'), nullable=False),
        Column("programmed_date", DateTime),
        Column("sent_date", DateTime),
        Column("created", DateTime, nullable=False,
               default=datetime.datetime.now),
        Column("modified", DateTime, nullable=False,
               default=datetime.datetime.now),
    )

    groups = orm.relation(Group, secondary=GroupSentMailing.__table__)
    mailing = orm.relation(Mailing,
        backref=orm.backref('sent_mailings', cascade='all,delete-orphan'),
        innerjoin=True,
        )

    @declared_attr
    def recipients(cls):
        _recipient_join = GroupSentMailing.__table__.join(
            Group.__table__.join(Recipient.__table__).alias('group_recipient')
            ).alias('group_sent_mailing_group_recipient')

        return orm.relation(Recipient,
            secondary=_recipient_join,
            viewonly=True,
            lazy=True,
            order_by=[c for c in _recipient_join.c if 'priority' in c.name]
            )

    processed_recipients = orm.relation(Recipient,
        secondary=SentMailingProcessedRecipient.__table__,
        order_by=SentMailingProcessedRecipient.__table__.c.time,
        lazy=True
        )

    @property
    def unprocessed_recipients(self):
        processed = set(self.processed_recipients)
        return [r for r in self.recipients if r not in processed]


    @classmethod
    def least_recently_created(cls):
        return cls.query.order_by(sql.desc(cls.created)).first()

    def __json__(self):
        return dict(
            id=self.id,
            mailing_id=self.mailing_id,
            programmed_date=(self.programmed_date.isoformat()
                             if self.programmed_date else None),
            sent_date=self.sent_date.isoformat() if self.sent_date else None,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
        )



class Plugin(object):
    name = 'sqlalchemy'
    api = 2

    def __init__(self, engine, **kw):
        Session.configure(**dict(kw, bind=engine))

    def setup(self, app):
        pass

    def close(self):
        pass

    def apply(self, callback, route):
        def wrapper(*args, **kw):
            try:
                return callback(*args, **kw)
            finally:
                Session.remove()
        return wrapper
