import datetime
from itertools import groupby
from operator import attrgetter

from sqlalchemy import Table, Column, ForeignKey, DateTime, Integer, orm, sql
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.orderinglist import ordering_list

from . import Model, Session
from .item import Item
from .config import Config
from .template import Template
from .recipient import Group, Recipient

class FileLookupError(LookupError):
    pass

class MissingTemplate(FileLookupError):
    pass

class MailingTemplate(Model):
    __tablename__ = "mailing_template"

    mailing_id = Column(ForeignKey('mailing.id', ondelete='CASCADE'),
                       primary_key=True)
    template_id = Column(ForeignKey('template.id', ondelete='CASCADE'),
                         primary_key=True)

    def __json__(self):
        return dict(
            id='::'.join(map(str, [self.mailing_id, self.template_id])),
            template_id=self.template_id,
            mailing_id=self.mailing_id,
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
    templates = orm.relation(Template, secondary=MailingTemplate.__table__,
                             collection_class=attribute_mapped_collection('type'),
                             lazy=True)


    @classmethod
    def by_number(cls, number, eager=True):
        q = cls.query.filter_by(number=number)
        if eager:
            q = q.options(
                orm.joinedload_all('items.image'),
                orm.joinedload_all('templates.images'),
                orm.joinedload_all('items.category.image'),
                orm.joinedload_all('items.category.subcategories'),
            )
        try:
            return q.one()
        except NoResultFound:
            return None

    @classmethod
    def least_recently_created(cls):
        return cls.query.order_by(sql.desc(cls.created)).first()

    @classmethod
    def next_number(cls):
        query = sql.select([sql.func.max(cls.number)])
        return (Session.execute(query).scalar() or 0) + 1

    @property
    def grouped_items(self):
        return groupby(self.items, attrgetter('category'))

    @property
    def url(self):
        tpl = Config.setdefault('mailing.external_url_template', '')
        if tpl:
            return tpl.format(number=self.number)
        else:
            base = Config.setdefault('server.external_base_url',
                                     'http://localhost:8080')
            return base + self.internal_url


    @property
    def internal_url(self):
        from ..web import get_url
        return get_url('mailing_file', number=self.number, filename='')

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
            internal_url = self.internal_url,
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
    __table__ = Table('sent_mailing_processed_recipient', Model.metadata,
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
    __table__ = Table('sent_mailing', Model.metadata,
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

