#coding: utf8
import os, os.path
from itertools import groupby, chain
from operator import attrgetter
import textwrap
import datetime

from babel.dates import format_date

from lxml import etree, builder

import markdown

from pkg_resources import resource_filename

from sqlalchemy import  Column, ForeignKey, DateTime, Integer, Unicode, orm,\
                        Table, LargeBinary, String, create_engine, MetaData, sql
from sqlalchemy.orm import deferred
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.hybrid import hybrid_property

from .util import sniff_content_type

def create_sessionmaker(dburl="sqlite:///:memory:", create_tables=True,
                        echo=True):
    engine = create_engine(dburl, echo=echo)
    if create_tables:
        Model.metadata.create_all(engine)
    return orm.sessionmaker(bind=engine)
    
metadata = MetaData()
Model = declarative_base(metadata=metadata)

class MissingTemplate(StandardError):
    pass

class Image(Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    filename = Column(Unicode(255), nullable=False)
    title = Column(Unicode(512))
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    _data = deferred(Column('data', LargeBinary(), nullable=False))
    content_type = Column(String(20), nullable=False)

    @hybrid_property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self.content_type = sniff_content_type(value)
        self._data = value

    @data.expression
    def data(cls):
        return cls._data

    def __repr__(self):
        data = (self.id, self.title, self.filename)
        return self.__class__.__name__ + repr(data)

    def __json__(self):
        return dict(
            id=self.id,
            title=self.title,
            filename=self.filename,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
            )

class Category(Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    image_id = Column(Integer, ForeignKey("image.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

    image = orm.relation(Image, lazy=True)
    subcategories = orm.relation("Category",
        backref = orm.backref('category', remote_side=[id],
                              lazy='joined', join_depth=3))
                            

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
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    mailing_id = Column(Integer, ForeignKey('mailing.id', ondelete='CASCADE',
                                            onupdate='CASCADE'),
                       nullable=False)

    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'Item',
                       'with_polymorphic': '*'}

    category = orm.relation(Category, backref='items', lazy=True)

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
            )

class ExternalLink(Item):
    __tablename__ = "external_link"
    id = Column(Integer, ForeignKey("item.id"), primary_key=True)
    url = Column(Unicode, nullable=False)
    text = Column(Unicode)
    __mapper_args__ = {'polymorphic_identity':'ExternalLink'}

    def __json__(self):
        return dict(super(ExternalLink, self).__json__(),
            text = self.text,
            url = self.url,
            )

class Article(Item):
    __tablename__ = "article"
    id = Column(Integer, ForeignKey("item.id"), primary_key=True)
    image_id = Column(Integer, ForeignKey("image.id"))

    text = Column(Unicode, nullable=False)
    image = orm.relation(Image)
    image_position = Column(String(1), nullable=False, default="l")

    __mapper_args__ = {'polymorphic_identity':'Article'}

    @property
    def url(self):
        return "#art-%d"%self.position

    @property
    def anchor(self):
        return "art-%d"%self.position


    @property
    def html(self):
        dom = etree.HTML('<div>%s</div>' % markdown.markdown(self.text))
        self._insert_image(dom)
        return '\n'.join(etree.tounicode(e, method='xml')
                         for e in dom.getchildren())

    def plain_text(self, width=79):
        dom = etree.HTML('<div>%s</div>' % markdown.markdown(self.text))
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
                img = builder.E.img(src=self.image.filename,
                                    title=self.image.title,
                                    alt=self.image.title)
                class_ = 'left' if self.image_position=='l' else 'right'
                img.attrib["class"] = class_
                p.insert(0, img)
                img.tail = p.text
                p.text = None

    def __json__(self):
        return dict(super(Article, self).__json__(),
            image_id = self.image_id,
            image_position = self.image_position,
            text = self.text,
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
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    title = Column(Unicode, nullable=False)
    type = Column(String(20), nullable=False, default='xhtml')
    body = Column(Unicode, nullable=False)

    images = orm.relation(Image, secondary=template_image_table, lazy=True)

    variables =  dict(
        format_date = format_date
        )

    @classmethod
    def latest_by_type(cls, session, type):
        q =session.query(cls).filter_by(type=type)
        q = q.order_by(sql.desc(cls.modified))
        return q.first()


    def __repr__(self):
        data = (self.id, self.title)
        return self.__class__.__name__ + repr(data)

    def render(self, **data):
        namespace = dict(self.variables, **data)
        if self.type == 'text':
            from mako.template import Template
            module_directory = '/tmp/mako_templates' #FIXME
            tpl = Template(self.body,
                module_directory=module_directory,
                default_filters=['decode.utf8'],
                )
            return tpl.render_unicode(**namespace)
        else:
            from genshi.template import MarkupTemplate
            tpl = MarkupTemplate(self.body)
            stream = tpl.generate(**namespace)
            return stream.render(self.type).decode('utf8') #FIXME: Derive from <meta http-equiv> if present
        

class Group(Model):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)

    def __repr__(self):
        data = (self.id, self.title)
        return self.__class__.__name__ + repr(data)

    def __json__(self):
        return dict(
            id=self.id,
            title=self.title,
            )

class Recipient(Model):
    __tablename__ = "recipient"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"))

    group = orm.relation(Group, backref="recipients")
    
    def __repr__(self):
        data = (self.id, self.name, self.email)
        return self.__class__.__name__ + repr(data)


    def __json__(self):
        return dict(
            id=self.id,
            name=self.name,
            email=self.email,
            group_id=self.group_id,
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
    date = Column(DateTime, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)

    items = orm.relation(Item, collection_class=ordering_list('position'),
                         order_by=Item.position, backref='mailing',
                         lazy=True, cascade='all,delete-orphan')
    templates = orm.relation(Template, secondary=mailing_template_table,
                             collection_class=attribute_mapped_collection('type'),
                             lazy=True)


    @classmethod
    def next_number(cls, session):
        query = sql.select([sql.func.max(cls.number)])
        return session.execute(query).scalar() + 1

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
            if i.category.image:
                images.add(i.category.image)
            if hasattr(i, 'image') and i.image is not None:
                images.add(i.image)
        return list(images)

    def get_file(self, filename):
        try:
            return [i for i in self.images if i.filename==filename][0]
        except IndexError:
            raise LookupError(filename)

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
        
group_sent_mailing_table = Table("group_sent_mailing", Model.metadata,
    Column('group_id', Integer, ForeignKey('group.id', ondelete="CASCADE"),
            primary_key=True),
    Column('sent_mailing_id', Integer,
           ForeignKey('sent_mailing.id', ondelete="CASCADE"),
           primary_key=True)
)
recipient_sent_mailing_table = Table("recipient_sent_mailing", Model.metadata,
    Column('recipient_id', Integer, ForeignKey('recipient.id', ondelete="CASCADE"),
            primary_key=True),
    Column('sent_mailing_id', Integer,
           ForeignKey('sent_mailing.id', ondelete="CASCADE"),
           primary_key=True)
)

class SentMailing(Model):
    __tablename__ = 'sent_mailing'

    id = Column(Integer, primary_key=True)
    mailing_id = Column(Integer, ForeignKey('mailing.id'),
                      nullable=False)
    time = Column(DateTime, nullable=False, default=datetime.datetime.now)
    groups = orm.relation(Group, secondary=group_sent_mailing_table)
    recipients = orm.relation(Recipient, secondary=recipient_sent_mailing_table)

    mailing = orm.relation(Mailing)

    @property
    def all_recipients(self):
        return chain(self.recipients, *(g.recipients for g in self.groups))
