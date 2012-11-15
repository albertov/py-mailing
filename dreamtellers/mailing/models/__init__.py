#coding: utf8
import datetime

from sqlalchemy import event, create_engine, orm
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()
Session = orm.scoped_session(
    orm.sessionmaker(autoflush=False, autocommit=False)
    )
Model.query = Session.query_property()

from .config import Config
from .template import Template
from .image import Image
from .item import Category, Item
from .content import Article, ExternalLink
from .recipient import Group, Recipient
from .mailing import (Mailing, SentMailing, GroupSentMailing, FileLookupError,
                      MissingTemplate)


__all__ = [
    "create_engine",
    "Model",
    "Session",
    "Image",
    "Config",
    "Template",
    "Category",
    "Item",
    "Article",
    "ExternalLink",
    "Group",
    "Recipient",
    "Mailing",
    "SentMailing",
    "GroupSentMailing",
    "FileLookupError",
    "MissingTemplate",
]





@event.listens_for(orm.mapper, 'before_update')
def update_modified_time(mapper, connection, instance):
    if hasattr(mapper.c, 'modified'):
        instance.modified = datetime.datetime.now()



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
