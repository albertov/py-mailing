#coding: utf8
import os, os.path
from itertools import groupby
from operator import attrgetter

from babel.dates import format_date

from genshi import template

import markdown

from pkg_resources import resource_filename

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, ForeignKey, DateTime, Integer, Unicode, orm,\
                        Table, create_engine
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
    path = Column(Unicode(255), nullable=False)
    title = Column(Unicode(512))

    @property
    def abspath(self):
        return os.path.join(os.environ.get(IMAGE_DIR_KEY, ''), self.path)
    
    def __repr__(self):
        data = (self.id, self.title, self.path)
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


class Template(Model):
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    type = Column(Unicode(20), nullable=False)
    serializer = Column(Unicode(20), nullable=False, default='xhtml')
    _data = Column('data', Unicode, nullable=False)
    __mapper_args__ = {'polymorphic_on':type,
                       'polymorphic_identity':'Template'}
    body = orm.synonym('_data')

    variables =  dict(
        format_date = format_date
        )


    def __repr__(self):
        data = (self.id, self.title)
        return self.__class__.__name__ + repr(data)

    @property
    def _template(self):
        if self.serializer == 'text':
            return template.TextTemplate(self.body)
        else:
            return template.MarkupTemplate(self.body)

    def render(self, **data):
        stream = self._template.generate(**dict(self.variables, **data))
        if self.serializer == 'text':
            return unicode(stream)
        else:
            return stream.render(self.serializer)
        

class FilesystemTemplate(Template):
    path = orm.synonym('_data')
    __mapper_args__ = {'polymorphic_identity':'FilesystemTemplate'}

    @property
    def abspath(self):
        return resource_filename(__name__, 'templates/'+self.path)


    @property
    def body(self):
        with open(self.abspath) as f:
            return f.read()

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
    Column('group', Integer, ForeignKey('group.id', ondelete="CASCADE")),
    Column('mailing', Integer, ForeignKey('mailing.number', ondelete="CASCADE"))
)

class Mailing(Model):
    __tablename__ = "mailing"

    number = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    send_date = Column(DateTime)
    _template = Column("template", Integer, ForeignKey("template.id"))

    template = orm.relation(Template)
    items = orm.relation(Item, collection_class=ordering_list('position'),
                         order_by=Item.position, backref='mailing',
                         lazy=False)
    groups = orm.relation(Group, secondary=group_mailing_table)

    @property
    def grouped_items(self):
        return groupby(self.items, attrgetter('category'))

    def items_by_type(self, type):
        return (i for i in self.items if i.type==type)

    def render(self, format='xhtml'):
        return self.template.render(mailing=self)

    def __repr__(self):
        data = (self.number, self.date, len(self.items))
        return self.__class__.__name__ + repr(data)

