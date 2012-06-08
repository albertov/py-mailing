#coding: utf8
from itertools import groupby
from operator import attrgetter

import markdown

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, ForeignKey, DateTime, Integer, Unicode, orm,\
                        Table, create_engine
from sqlalchemy.ext.orderinglist import ordering_list


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
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    title = Column(Unicode(512))
    

class Category(Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    _image = Column("image", Integer, ForeignKey("image.id"))
    image = orm.relation(Image)

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


    def __html__(self):
        return markdown.markdown(self.text)

class Template(Model):
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    type = Column(Unicode(20), nullable=False)
    _data = Column('data', Unicode, nullable=False)
    __mapper_args__ = {'polymorphic_on':type,
                       'polymorphic_identity':'Template'}
    body = orm.synonym('_data')

class FilesystemTemplate(Template):
    path = orm.synonym('_data')
    __mapper_args__ = {'polymorphic_identity':'FilesystemTemplate'}


class Group(Model):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)

class Recipient(Model):
    __tablename__ = "recipient"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False)
    _group = Column("group", Integer, ForeignKey("group.id"))

    group = orm.relation(Group, backref="recipients")

group_mailing_table = Table("group_mailing", Model.metadata,
    Column('group', Integer, ForeignKey('group.id', ondelete="CASCADE")),
    Column('mailing', Integer, ForeignKey('mailing.number', ondelete="CASCADE"))
)
    

class Mailing(Model):
    __tablename__ = "mailing"

    number = Column(Integer, primary_key=True)
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

    @property
    def formatted_number(self):
        return u"nº {03}".format(self.number)
