import datetime
from cStringIO import StringIO
from hashlib import md5

import Image as PILImage

from sqlalchemy import (Column, DateTime, Integer, Unicode, orm,
                        LargeBinary, String, Binary)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.exc import NoResultFound


from . import Model
from .util import HexBinaryComparator
from .config import Config


class Image(Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    _hash = Column('hash', Binary(16), unique=True, nullable=False)
    filename = Column(Unicode(255), nullable=False, unique=True)
    title = Column(Unicode(512))
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified = Column(DateTime, nullable=False, default=datetime.datetime.now)
    _data = orm.deferred(Column('data', LargeBinary(), nullable=False))
    content_type = Column(String(20), nullable=False)

    PIL_MAP = {
        'image/jpeg': 'JPEG',
        'image/gif': 'GIF',
        'image/png': 'PNG',
    }


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
        self.content_type = self._get_content_type(value)
        self.hash = md5(value).hexdigest()
        self._data = value

    @data.expression
    def data_expr(cls):
        return cls._data

    @hybrid_property
    def hash(self):
        return self._hash.encode('hex')

    @hash.setter
    def hash(self, value):
        self._hash = value.decode('hex')

    @hash.expression
    def hash(cls):
        return cls._hash

    @hash.comparator
    def hash(cls):
        return HexBinaryComparator(cls._hash)

    @property
    def url(self):
        base = Config.setdefault('server.external_base_url',
                                 'http://localhost:8080')
        return base + self.internal_url

    @property
    def internal_url(self):
        from .. import get_url
        return get_url('image_view', hash=self.hash)

    def thumbnail(self, width, height):
        img = _pil_image(self.data)
        img.thumbnail((width, height), PILImage.ANTIALIAS)
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
    def _get_content_type(cls, data):
        im = _pil_image(data)
        if im is not None:
            for k,v in cls.PIL_MAP.iteritems():
                if v==im.format:
                    return k
        
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

def _pil_image(data):
    try:
        return PILImage.open(StringIO(data))
    except IOError:
        # not an image
        return None
