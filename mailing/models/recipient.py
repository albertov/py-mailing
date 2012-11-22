import datetime

from sqlalchemy import Column, ForeignKey, DateTime, Integer, Unicode, orm

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


