#coding: utf8
import os, os.path
from itertools import groupby
from operator import attrgetter

from babel.dates import format_date

from genshi import template

import markdown

from pkg_resources import resource_filename

from sqlalchemy import  Column, ForeignKey, DateTime, Integer, Unicode, orm,\
                        Table, LargeBinary, create_engine
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list

IMAGE_DIR_KEY = 'DT_IMAGE_DIR'

def create_sessionmaker(dburl="sqlite:///:memory:", create_tables=True,
                        echo=True):
    engine = create_engine(dburl, echo=echo)
    if create_tables:
        Model.metadata.create_all(engine)
    return orm.sessionmaker(bind=engine)
    
Model = declarative_base()

class Image(Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    filename = Column(Unicode(255), nullable=False)
    title = Column(Unicode(512))
    data = Column(LargeBinary(), nullable=False)

    def __repr__(self):
        data = (self.id, self.title, self.filename)
        return self.__class__.__name__ + repr(data)

class Category(Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    _image = Column("image", Integer, ForeignKey("image.id"))
    image = orm.relation(Image)

    def __repr__(self):
        data = (self.id, self.title, self.image)
        return self.__class__.__name__ + repr(data)


class Item(Model):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    type = Column(Unicode(20), nullable=False)
    position = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    _mailing = Column("mailing", Integer, ForeignKey('mailing.number'),
                       nullable=False)
    _data = Column('data', Unicode, nullable=False)

    __mapper_args__ = {'polymorphic_on':type, 'polymorphic_identity':'Item'}

    category = orm.relation(Category, backref='items', lazy=False)

    def __repr__(self):
        data = (self.id, self.title, self.category.title)
        return self.__class__.__name__ + repr(data)


class ExternalLink(Item):
    url = orm.synonym('_data')
    __mapper_args__ = {'polymorphic_identity':'ExternalLink'}

class Article(Item):
    __tablename__ = "article"
    id = Column(Integer, ForeignKey("item.id"), primary_key=True)
    _image = Column("image", Integer, ForeignKey("image.id"))

    text = orm.synonym('_data')
    image = orm.relation(Image)
    image_position = Column(Unicode(1), nullable=False, default="l")

    __mapper_args__ = {'polymorphic_identity':'Article'}

    @property
    def url(self):
        return "#%d"%self.position

    @property
    def anchor(self):
        return "%d"%self.position


    @property
    def html(self):
        return markdown.markdown(self.text)

template_image_table = Table("template_image", Model.metadata,
    Column('template', Integer, ForeignKey('template.id', ondelete="CASCADE")),
    Column('image', Integer, ForeignKey('image.id', ondelete="CASCADE"))
)

class Template(Model):
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    type = Column(Unicode(20), nullable=False, default='xhtml')
    body = Column(Unicode, nullable=False)

    images = orm.relation(Image, secondary=template_image_table)

    variables =  dict(
        format_date = format_date
        )


    def __repr__(self):
        data = (self.id, self.title)
        return self.__class__.__name__ + repr(data)

    @property
    def _template(self):
        if self.type == 'text':
            return template.TextTemplate(self.body)
        else:
            return template.MarkupTemplate(self.body)

    def render(self, **data):
        stream = self._template.generate(**dict(self.variables, **data))
        if self.type == 'text':
            return unicode(stream)
        else:
            return stream.render(self.serializer)
        

class Group(Model):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)

    def __repr__(self):
        data = (self.id, self.title)
        return self.__class__.__name__ + repr(data)


class Recipient(Model):
    __tablename__ = "recipient"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False)
    _group = Column("group", Integer, ForeignKey("group.id"))

    group = orm.relation(Group, backref="recipients")
    
    def __repr__(self):
        data = (self.id, self.name, self.email)
        return self.__class__.__name__ + repr(data)



group_mailing_table = Table("group_mailing", Model.metadata,
    Column('group', Integer, ForeignKey('group.id', ondelete="CASCADE"),
            primary_key=True),
    Column('mailing', Integer, ForeignKey('mailing.number', ondelete="CASCADE"),
           primary_key=True)
)


mailing_template_table = Table("mailing_template", Model.metadata,
   Column('mailing', ForeignKey('mailing.number', ondelete='CASCADE'),
          primary_key=True),
    Column('template', ForeignKey('template.id', ondelete='CASCADE'),
           primary_key=True)
)
                            

class Mailing(Model):
    __tablename__ = "mailing"

    number = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    send_date = Column(DateTime)

    items = orm.relation(Item, collection_class=ordering_list('position'),
                         order_by=Item.position, backref='mailing',
                         lazy=False)
    groups = orm.relation(Group, secondary=group_mailing_table)
    templates = orm.relation(Template, secondary=mailing_template_table,
                             collection_class=attribute_mapped_collection('type'))

    @property
    def grouped_items(self):
        return groupby(self.items, attrgetter('category'))

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

    def items_by_type(self, type):
        return [i for i in self.items if i.type==type]

    def render(self, format='xhtml'):
        return self.templates['format'].render(mailing=self)

    def __repr__(self):
        data = (self.number, self.date, len(self.items))
        return self.__class__.__name__ + repr(data)

