from UserDict import DictMixin

from sqlalchemy import Column, String, Unicode, Enum
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.hybrid import hybrid_property

from . import Model, Session


class Config(Model):
    __tablename__ = "config"
    __type_names__ = ("int", "float", "str", "unicode", "bool")
    _key = Column("key", String(128), primary_key=True)
    _value = Column("value", Unicode, nullable=False)
    type = Column(Enum(*__type_names__), default="unicode", nullable=False)
    

    class __metaclass__(DictMixin, DeclarativeMeta):
            
        def __getitem__(cls, key):
            ob = cls.query.get(key)
            if ob is None:
                raise KeyError(key)
            return ob.value

        def __setitem__(cls, key, value):
            ob = cls.query.get(key)
            if ob is not None:
                ob.value = value
            else:
                ob = cls(key, value)
                Session.add(ob)
                Session.flush()

        def __delitem__(cls, key):
            ob = cls.query.get(key)
            if ob is not None:
                Session.delete(ob)
                Session.flush()
            else:
                raise KeyError(key)

        def __json__(cls):
            return dict(cls)

        def __contains__(cls, key):
            return bool(cls.query.get(key))

        def __iter__(cls):
            return (c.key for c in cls.query)

        def iteritems(cls):
            return ((c.key, c.value) for c in cls.query)
            
        def keys(cls):
            return [c.key for c in cls.query]
            

    def __init__(self, key, value):
        self.key = key
        self.value = value

    @hybrid_property
    def key(self):
        return self._key

    @key.setter
    def _key_setter(self, key):
        if type(key) is not str:
            raise TypeError("Only str keys are allowed")
        self._key = key


    @hybrid_property
    def value(self):
        if self.type!='bool':
            cast = __builtins__[self.type]
            return cast(self._value)
        else:
            return self._value != 'False'

    @value.setter
    def _value_setter(self, value):
        self.type = type(value).__name__
        if self.type not in self.__type_names__:
            raise TypeError
        self._value = unicode(value)
