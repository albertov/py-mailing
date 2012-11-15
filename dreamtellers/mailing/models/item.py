import datetime

from sqlalchemy import (Column, ForeignKey, DateTime, Integer, Unicode,
                        String, orm, event)

from . import Model
from .image import Image


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

    category = orm.relation(Category,
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
    from . import Mailing
    stmt = Mailing.__table__.update().where(Mailing.id==instance.mailing_id)
    stmt = stmt.values(modified=datetime.datetime.now())
    connection.execute(stmt)

