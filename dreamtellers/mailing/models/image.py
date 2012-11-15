import datetime
from cStringIO import StringIO
from hashlib import md5

import Image as PILImage

from sqlalchemy import (Column, DateTime, Integer, Unicode, orm,
                        LargeBinary, String)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.exc import NoResultFound

from ..util import sniff_content_type

from . import Model


class Image(Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    hash = Column(String(32), unique=True, nullable=False)
    filename = Column(Unicode(255), nullable=False, unique=True)
    title = Column(Unicode(512))
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    _data = orm.deferred(Column('data', LargeBinary(), nullable=False))
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
        base = Config.setdefault('server.external_base_url',
                                 'http://localhost:8080')
        return base + self.internal_url

    @property
    def internal_url(self):
        from ..web import app
        return app.get_url('image_view', hash=self.hash)

    PIL_MAP = {
        'image/jpeg': 'JPEG',
        'image/gif': 'GIF',
        'image/png': 'PNG',
    }
    def thumbnail(self, width, height):
        img = PILImage.open(StringIO(self.data))
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
        img = PILImage.new('RGBA', (width, height))
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
            internal_url=self.internal_url,
            )

