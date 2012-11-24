import datetime

from sqlalchemy import (Column, ForeignKey, DateTime, Integer, Unicode, orm,
                        Boolean, sql)
from sqlalchemy.orm.exc import NoResultFound

from . import Model



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
    email = Column(Unicode, nullable=False, unique=True)
    group_id = Column(Integer, ForeignKey("group.id"))
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    active = Column(Boolean, default=True, nullable=False)
    error = Column(Boolean, default=False, nullable=False)

    group = orm.relation(Group,  backref='recipients')

    @property
    def bounces_query(self):
        from .mailing import MailingDeliveryProcessedRecipient as D
        return self.deliveries.filter(D.bounce_time!=None)

    @classmethod
    def by_email(cls, email):
        try:
            return cls.query.filter_by(email=email).one()
        except NoResultFound:
            return None
    
    def __repr__(self):
        data = (self.id, self.name, self.email)
        return self.__class__.__name__ + repr(data)


    def __json__(self):
        return dict(
            id=self.id,
            name=self.name,
            email=self.email,
            active=self.active,
            error=self.error,
            group_id=self.group_id,
            created=self.created.isoformat() if self.created else None,
            modified=self.modified.isoformat() if self.modified else None,
            )
